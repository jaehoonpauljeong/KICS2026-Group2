import rich
import sys
from pydantic import BaseModel
from openai import OpenAI
from validate import validate_xml_full_report

import json
from config import (
    OPENAI_API_KEY,
    RFC5646_LANGUAGE_TAGS,
    yang_instruct,
    condition_instruct,
    action_instruct,
    endpoint_instruct,
    threat_instruct
)
# read json to dictionary
with open('region.json', 'r', encoding='utf-8') as f:
    REGION_CODE = json.load(f)

model = 'gpt-5'
client = OpenAI(api_key=OPENAI_API_KEY)

class PolicyRequest(BaseModel):
    action: str
    target: str
    start_time: str | None
    end_time: str | None
    days: list[str] | None
    frequency: str | None
    description: str

class EndpointGroupRequest(BaseModel):
    user_group: str | None
    device_group: str | None
    
class Tasks(BaseModel):
    policies: list[PolicyRequest]
    endpoint_groups: list[EndpointGroupRequest] | None

def extract_requests(policy_text: str, model) -> Tasks:
    response = client.chat.completions.create(
        model=model,
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are an expert in extracting structured data from natural language."},
            {"role": "user", "content": [
                {"type": "text", "text":
             f"""Extract the policy requests from the following text into structured format: {policy_text} knowing that:
             - the time should be in HH:MM format
             - days should be full names like Monday, Tuesday, etc.
             - frequency should be one of: only-once, weekly, monthly, yearly
             - target is the entity to which the policy is applied, often an endpoint group, user group, device group, or specific IP addresses. if not specified, use "any".
             - action should be one of: 
              - pass : allows traffic that matches the rule to proceed through
              - drop : denies the traffic that matches the rule.
              - reject : denies a packet to go through
              - rate-limit : limits the number of packets or flows that can go through
              - mirror : copies a packet and sends the packet's copy to the monitoring entity

              Json format: {Tasks.model_json_schema()}
             """}]
            }
        ],
        temperature=0.0,
    )

    tasks = Tasks.model_validate_json(response.choices[0].message.content)
    return tasks

class Region(BaseModel):
    city_name: str
    region_code: str

class Country(BaseModel):
    name: str
    region: list[Region]
    
class GeoData(BaseModel):
    country: list[Country] | None

def geo_collect(tasks, model) -> GeoData:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an expert in collectiong important geographical data."},
            {"role": "user", "content": f"""
             From this data: {REGION_CODE} and the tasks: {tasks}, extract the countries and the cities mentioned in the tasks.
             region_code is the subdivision_code_iso3166-2 from the data. it is the code for each city.
             if None mentioned, return empty list.
             country is in [ISO 3166-1 alpha-2 code, e.g., "US"]
             region is in [ISO 3166-2 code, e.g., "US-CA"]
             city is in [City name in English, e.g., "San Francisco"]
             Json format: {GeoData.model_json_schema()}
             """
            }
        ]
    )

    geo_data = GeoData.model_validate_json(response.choices[0].message.content)
    return geo_data


class Step(BaseModel):
    description: str
    explanation: str
    reason_of_this_step: str
    xml_snippet: str

class GenerationResponse(BaseModel):
    steps: list[Step]
    final_xml_policy: str
    endpoint_xml: str | None
    threatfeed_xml: str | None

def generate_policy(tasks, model="gpt-4o-mini", geo_data=None) -> GenerationResponse:
    """
    Converts natural language policy into an XML security policy.
    Includes an example and IETF draft content for context.
    """
    # Examples to guide the model
    example_input1 = "Block my son's computers from malicious websites."
    example_output1 = """
<?xml version="1.0" encoding="UTF-8" ?>
<i2nsf-cfi-policy
    xmlns="urn:ietf:params:xml:ns:yang:ietf-i2nsf-cfi-policy">
    <name>block_web_security_policy</name>
    <rules>
        <name>block_web</name>
        <condition>
            <firewall-condition>
                <source>Son's_PC</source>
            </firewall-condition>
            <url-condition>
                <url-name>malicious_websites</url-name>
            </url-condition>
        </condition>
        <actions>
            <primary-action>
                <action>drop</action>
            </primary-action>
        </actions>
    </rules>
</i2nsf-cfi-policy>
    """

    example_input2 = "Block malicious VoIP/VoCN packets coming to a company."
    example_output2 = """
<?xml version="1.0" encoding="UTF-8" ?>
<i2nsf-cfi-policy
    xmlns="urn:ietf:params:xml:ns:yang:ietf-i2nsf-cons-facing-interface">
    <name>
        security_policy_for_blocking_malicious_voip_packets
    </name>
    <rules>
        <name>Block_malicious_voip_and_vocn_packets</name>
        <condition>
            <voice>
                <source-id>malicious-id</source-id>
            </voice>
            <firewall>
                <destination>employees</destination>
            </firewall>
        </condition>
        <action>
            <primary-action>
                <action>drop</action>
            </primary-action>
        </action>
    </rules>
</i2nsf-cfi-policy>
    """

    example_input3 = "Mitigate flood attacks on a company web server."
    example_output3 = """
<?xml version="1.0" encoding="UTF-8" ?>
<i2nsf-cfi-policy
    xmlns="urn:ietf:params:xml:ns:yang:ietf-i2nsf-cons-facing-interface">
    <name>security_policy_for_ddos_attacks</name>
    <rules>
        <name>1000_packets_per_second</name>
        <condition>
            <firewall>
                <destination>webservers</destination>
            </firewall>
            <ddos>
                <rate-limit>
                    <packet-rate-threshold>1000</packet-rate-threshold>
                </rate-limit>
            </ddos>
        </condition>
        <action>
            <primary-action>
                <action>drop</action>
            </primary-action>
        </action>
    </rules>
</i2nsf-cfi-policy>
    """

    # Load additional context from I2NSF's official IETF draft

    assist = f"""
    You are an XML schema and I2NSF policy expert.

    Here is a few examples for reference:
    Input: {example_input1}
    Output: {example_output1}

    Input: {example_input2}
    Output: {example_output2}

    Input: {example_input3}
    Output: {example_output3}

    Additional Context:
    for generating XML policy, follow the bellow instructions:
    {yang_instruct}
    {condition_instruct}
    {action_instruct}

    generate the endpoint groups and threatfeeds if needed. this is the instruction for that:
    {endpoint_instruct}
    {threat_instruct}
    if there is not much information about endpoint groups or threatfeeds, generate sample ones.

    """
    

    # Combine all elements into the prompt
    prompt = f"""
    Now, generate the XML for the following input:
    Input: {tasks}
    Geo Data: {geo_data}

    """
    
    response = client.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": f"{assist}"},
            {"role": "user", "content": prompt}
        ],
        reasoning_effort="medium",
        response_format=GenerationResponse
    )
    
    return response.choices[0].message

class FeedbackResponse(BaseModel):
    feedback: str
    valid: bool

def verify_policy(policy_text, endpoint_xml, threatfeed_xml, tasks, model="gpt-4o-mini", geo_data=None) -> FeedbackResponse:
    """
    Converts natural language policy into an XML security policy.
    Includes an example and IETF draft content for context.
    """
    # Examples to guide the model
    example_input1 = "Block my son's computers from malicious websites."
    example_output1 = """
<?xml version="1.0" encoding="UTF-8" ?>
<i2nsf-cfi-policy
    xmlns="urn:ietf:params:xml:ns:yang:ietf-i2nsf-cfi-policy">
    <name>block_web_security_policy</name>
    <rules>
        <name>block_web</name>
        <condition>
            <firewall-condition>
                <source>Son's_PC</source>
            </firewall-condition>
            <url-condition>
                <url-name>malicious_websites</url-name>
            </url-condition>
        </condition>
        <actions>
            <primary-action>
                <action>drop</action>
            </primary-action>
        </actions>
    </rules>
</i2nsf-cfi-policy>
    """

    example_input2 = "Block malicious VoIP/VoCN packets coming to a company."
    example_output2 = """
<?xml version="1.0" encoding="UTF-8" ?>
<i2nsf-cfi-policy
    xmlns="urn:ietf:params:xml:ns:yang:ietf-i2nsf-cons-facing-interface">
    <name>
        security_policy_for_blocking_malicious_voip_packets
    </name>
    <rules>
        <name>Block_malicious_voip_and_vocn_packets</name>
        <condition>
            <voice>
                <source-id>malicious-id</source-id>
            </voice>
            <firewall>
                <destination>employees</destination>
            </firewall>
        </condition>
        <action>
            <primary-action>
                <action>drop</action>
            </primary-action>
        </action>
    </rules>
</i2nsf-cfi-policy>
    """

    example_input3 = "Mitigate flood attacks on a company web server."
    example_output3 = """
<?xml version="1.0" encoding="UTF-8" ?>
<i2nsf-cfi-policy
    xmlns="urn:ietf:params:xml:ns:yang:ietf-i2nsf-cons-facing-interface">
    <name>security_policy_for_ddos_attacks</name>
    <rules>
        <name>1000_packets_per_second</name>
        <condition>
            <firewall>
                <destination>webservers</destination>
            </firewall>
            <ddos>
                <rate-limit>
                    <packet-rate-threshold>1000</packet-rate-threshold>
                </rate-limit>
            </ddos>
        </condition>
        <action>
            <primary-action>
                <action>drop</action>
            </primary-action>
        </action>
    </rules>
</i2nsf-cfi-policy>
    """

    # Load additional context from I2NSF's official IETF draft

    assist = f"""
    You are an XML schema and I2NSF policy expert.

    Here is a few examples for reference:
    Input: {example_input1}
    Output: {example_output1}

    Input: {example_input2}
    Output: {example_output2}

    Input: {example_input3}
    Output: {example_output3}

    Additional Context:
    for generating XML policy, follow the bellow instructions:
    {yang_instruct}
    {condition_instruct}
    {action_instruct}

    generate the endpoint groups and threatfeeds if needed. this is the instruction for that:
    {endpoint_instruct}
    {threat_instruct}
    if there is not much information about endpoint groups or threatfeeds, generate sample ones.

    """
    

    # Combine all elements into the prompt
    prompt = f"""
    Now, verify the compliance of the following XML policy with the I2NSF schema.
    Containing the generated XML policy and the tasks.
    pseudo policy: {policy_text}
    tasks: {tasks}

    this is the endpoint group xml: {endpoint_xml}
    this is the threatfeed xml: {threatfeed_xml}

    check if there are any discrepancies or missing elements.
    give feedback on the part that needs to be fixed.
     
    if the policy is compliant, respond with "The policy is compliant."
    Otherwise, provide specific feedback on what needs to be corrected.
    """
    
    response = client.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": f"{assist}"},
            {"role": "user", "content": prompt}
        ],
        reasoning_effort="medium",
        response_format=FeedbackResponse
    )
    
    return response.choices[0].message

def fix_policy(policy, endpoint_xml, threatfeed_xml, feedback, model="gpt-4o-mini", geo_data=None) -> GenerationResponse:
    """
    Converts natural language policy into an XML security policy.
    Includes an example and IETF draft content for context.
    """
    # Examples to guide the model
    example_input1 = "Block my son's computers from malicious websites."
    example_output1 = """
<?xml version="1.0" encoding="UTF-8" ?>
<i2nsf-cfi-policy
    xmlns="urn:ietf:params:xml:ns:yang:ietf-i2nsf-cfi-policy">
    <name>block_web_security_policy</name>
    <rules>
        <name>block_web</name>
        <condition>
            <firewall-condition>
                <source>Son's_PC</source>
            </firewall-condition>
            <url-condition>
                <url-name>malicious_websites</url-name>
            </url-condition>
        </condition>
        <actions>
            <primary-action>
                <action>drop</action>
            </primary-action>
        </actions>
    </rules>
</i2nsf-cfi-policy>
    """

    example_input2 = "Block malicious VoIP/VoCN packets coming to a company."
    example_output2 = """
<?xml version="1.0" encoding="UTF-8" ?>
<i2nsf-cfi-policy
    xmlns="urn:ietf:params:xml:ns:yang:ietf-i2nsf-cons-facing-interface">
    <name>
        security_policy_for_blocking_malicious_voip_packets
    </name>
    <rules>
        <name>Block_malicious_voip_and_vocn_packets</name>
        <condition>
            <voice>
                <source-id>malicious-id</source-id>
            </voice>
            <firewall>
                <destination>employees</destination>
            </firewall>
        </condition>
        <action>
            <primary-action>
                <action>drop</action>
            </primary-action>
        </action>
    </rules>
</i2nsf-cfi-policy>
    """

    example_input3 = "Mitigate flood attacks on a company web server."
    example_output3 = """
<?xml version="1.0" encoding="UTF-8" ?>
<i2nsf-cfi-policy
    xmlns="urn:ietf:params:xml:ns:yang:ietf-i2nsf-cons-facing-interface">
    <name>security_policy_for_ddos_attacks</name>
    <rules>
        <name>1000_packets_per_second</name>
        <condition>
            <firewall>
                <destination>webservers</destination>
            </firewall>
            <ddos>
                <rate-limit>
                    <packet-rate-threshold>1000</packet-rate-threshold>
                </rate-limit>
            </ddos>
        </condition>
        <action>
            <primary-action>
                <action>drop</action>
            </primary-action>
        </action>
    </rules>
</i2nsf-cfi-policy>
    """

    # Load additional context from I2NSF's official IETF draft

    assist = f"""
    You are an XML schema and I2NSF policy expert.

    Here is a few examples for reference:
    Input: {example_input1}
    Output: {example_output1}

    Input: {example_input2}
    Output: {example_output2}

    Input: {example_input3}
    Output: {example_output3}

    Additional Context:
    for generating XML policy, follow the bellow instructions:
    {yang_instruct}
    {condition_instruct}
    {action_instruct}

    generate the endpoint groups and threatfeeds if needed. this is the instruction for that:
    {endpoint_instruct}
    {threat_instruct}
    if there is not much information about endpoint groups or threatfeeds, generate sample ones.

    """
    

    # Combine all elements into the prompt
    prompt = f"""
    You have the policy that needs to be fixed:
    {policy} and the feedback is: {feedback}. This is the endpoint group xml: {endpoint_xml}. This is the threatfeed xml: {threatfeed_xml}.
    Now, generate the corrected XML policy:

    Output:
    """
    
    response = client.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": f"{assist}"},
            {"role": "user", "content": prompt}
        ],
        reasoning_effort="medium",
        response_format=GenerationResponse
    )
    
    return response.choices[0].message

if __name__ == "__main__":
    req = sys.argv[1] if len(sys.argv) > 1 else \
        "Block SNS access from Buenos Aires, Argentina to Seoul during Korea office hours (09:00-18:00 Korea time)"

    tasks = extract_requests(req, model='gpt-4o-2024-08-06')
    rich.print(tasks)

    # Need to use local model to avoid OpenAI JSON parsing issues
    geo_data = geo_collect(tasks, model=model)
    rich.print(geo_data)

    result = generate_policy(tasks, model=model, geo_data=geo_data)
    report = "Generated Policy Steps:\n"
    for step in result.parsed.steps:

        report += f"- {step.description}: {step.explanation}\n"
        report += f"  Reasoning: {step.reason_of_this_step}\n"
        report += f"  XML Snippet: {step.xml_snippet}\n\n"

    open("generated_policy.xml", "w", encoding="utf-8").write(result.parsed.final_xml_policy)
    

    while True:
        validation_report = validate_xml_full_report("generated_policy.xml", "i2nsf-cfi-policy.xsd")
        print(validation_report)
        verification = verify_policy(result.parsed.final_xml_policy, result.parsed.endpoint_xml, result.parsed.threatfeed_xml, tasks, model=model, geo_data=geo_data)
        feedback = verification.parsed.feedback
        print("Verification Feedback:")
        print(feedback)
        if verification.parsed.valid:
            print("Policy is compliant with I2NSF schema.")
            break
        else:
            print("Regenerating policy based on feedback...")
            result = fix_policy(result.parsed.final_xml_policy, result.parsed.endpoint_xml, result.parsed.threatfeed_xml, feedback, model=model, geo_data=geo_data)
            open("generated_policy.xml", "w", encoding="utf-8").write(result.parsed.final_xml_policy)

    for step in result.parsed.steps:
        print(f"Step: {step.description}")
        print(f"Explanation: {step.explanation}")
        print(f"Reasoning: {step.reason_of_this_step}")
        print(f"XML Snippet: {step.xml_snippet}")
        print("-----")
    if result.parsed.endpoint_xml:
        print("Endpoint Group XML:")
        print(result.parsed.endpoint_xml)
    if result.parsed.threatfeed_xml:
        print("Threatfeed XML:")
        print(result.parsed.threatfeed_xml)
    print("Final XML Policy:")
    print(result.parsed.final_xml_policy)
