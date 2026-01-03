OPENAI_API_KEY = open("token").read().strip()

RFC5646_LANGUAGE_TAGS = {
  'af': 'Afrikaans',
  'af-ZA': 'Afrikaans (South Africa)',
  'ar': 'Arabic',
  'ar-AE': 'Arabic (U.A.E.)',
  'ar-BH': 'Arabic (Bahrain)',
  'ar-DZ': 'Arabic (Algeria)',
  'ar-EG': 'Arabic (Egypt)',
  'ar-IQ': 'Arabic (Iraq)',
  'ar-JO': 'Arabic (Jordan)',
  'ar-KW': 'Arabic (Kuwait)',
  'ar-LB': 'Arabic (Lebanon)',
  'ar-LY': 'Arabic (Libya)',
  'ar-MA': 'Arabic (Morocco)',
  'ar-OM': 'Arabic (Oman)',
  'ar-QA': 'Arabic (Qatar)',
  'ar-SA': 'Arabic (Saudi Arabia)',
  'ar-SY': 'Arabic (Syria)',
  'ar-TN': 'Arabic (Tunisia)',
  'ar-YE': 'Arabic (Yemen)',
  'az': 'Azeri (Latin)',
  'az-AZ': 'Azeri (Latin) (Azerbaijan)',
  'az-Cyrl-AZ': 'Azeri (Cyrillic) (Azerbaijan)',
  'be': 'Belarusian',
  'be-BY': 'Belarusian (Belarus)',
  'bg': 'Bulgarian',
  'bg-BG': 'Bulgarian (Bulgaria)',
  'bs-BA': 'Bosnian (Bosnia and Herzegovina)',
  'ca': 'Catalan',
  'ca-ES': 'Catalan (Spain)',
  'cs': 'Czech',
  'cs-CZ': 'Czech (Czech Republic)',
  'cy': 'Welsh',
  'cy-GB': 'Welsh (United Kingdom)',
  'da': 'Danish',
  'da-DK': 'Danish (Denmark)',
  'de': 'German',
  'de-AT': 'German (Austria)',
  'de-CH': 'German (Switzerland)',
  'de-DE': 'German (Germany)',
  'de-LI': 'German (Liechtenstein)',
  'de-LU': 'German (Luxembourg)',
  'dv': 'Divehi',
  'dv-MV': 'Divehi (Maldives)',
  'el': 'Greek',
  'el-GR': 'Greek (Greece)',
  'en': 'English',
  'en-AU': 'English (Australia)',
  'en-BZ': 'English (Belize)',
  'en-CA': 'English (Canada)',
  'en-CB': 'English (Caribbean)',
  'en-GB': 'English (United Kingdom)',
  'en-IE': 'English (Ireland)',
  'en-JM': 'English (Jamaica)',
  'en-NZ': 'English (New Zealand)',
  'en-PH': 'English (Republic of the Philippines)',
  'en-TT': 'English (Trinidad and Tobago)',
  'en-US': 'English (United States)',
  'en-ZA': 'English (South Africa)',
  'en-ZW': 'English (Zimbabwe)',
  'eo': 'Esperanto',
  'es': 'Spanish',
  'es-AR': 'Spanish (Argentina)',
  'es-BO': 'Spanish (Bolivia)',
  'es-CL': 'Spanish (Chile)',
  'es-CO': 'Spanish (Colombia)',
  'es-CR': 'Spanish (Costa Rica)',
  'es-DO': 'Spanish (Dominican Republic)',
  'es-EC': 'Spanish (Ecuador)',
  'es-ES': 'Spanish (Spain)',
  'es-GT': 'Spanish (Guatemala)',
  'es-HN': 'Spanish (Honduras)',
  'es-MX': 'Spanish (Mexico)',
  'es-NI': 'Spanish (Nicaragua)',
  'es-PA': 'Spanish (Panama)',
  'es-PE': 'Spanish (Peru)',
  'es-PR': 'Spanish (Puerto Rico)',
  'es-PY': 'Spanish (Paraguay)',
  'es-SV': 'Spanish (El Salvador)',
  'es-UY': 'Spanish (Uruguay)',
  'es-VE': 'Spanish (Venezuela)',
  'et': 'Estonian',
  'et-EE': 'Estonian (Estonia)',
  'eu': 'Basque',
  'eu-ES': 'Basque (Spain)',
  'fa': 'Farsi',
  'fa-IR': 'Farsi (Iran)',
  'fi': 'Finnish',
  'fi-FI': 'Finnish (Finland)',
  'fo': 'Faroese',
  'fo-FO': 'Faroese (Faroe Islands)',
  'fr': 'French',
  'fr-BE': 'French (Belgium)',
  'fr-CA': 'French (Canada)',
  'fr-CH': 'French (Switzerland)',
  'fr-FR': 'French (France)',
  'fr-LU': 'French (Luxembourg)',
  'fr-MC': 'French (Principality of Monaco)',
  'gl': 'Galician',
  'gl-ES': 'Galician (Spain)',
  'gu': 'Gujarati',
  'gu-IN': 'Gujarati (India)',
  'he': 'Hebrew',
  'he-IL': 'Hebrew (Israel)',
  'hi': 'Hindi',
  'hi-IN': 'Hindi (India)',
  'hr': 'Croatian',
  'hr-BA': 'Croatian (Bosnia and Herzegovina)',
  'hr-HR': 'Croatian (Croatia)',
  'hu': 'Hungarian',
  'hu-HU': 'Hungarian (Hungary)',
  'hy': 'Armenian',
  'hy-AM': 'Armenian (Armenia)',
  'id': 'Indonesian',
  'id-ID': 'Indonesian (Indonesia)',
  'is': 'Icelandic',
  'is-IS': 'Icelandic (Iceland)',
  'it': 'Italian',
  'it-CH': 'Italian (Switzerland)',
  'it-IT': 'Italian (Italy)',
  'ja': 'Japanese',
  'ja-JP': 'Japanese (Japan)',
  'ka': 'Georgian',
  'ka-GE': 'Georgian (Georgia)',
  'kk': 'Kazakh',
  'kk-KZ': 'Kazakh (Kazakhstan)',
  'kn': 'Kannada',
  'kn-IN': 'Kannada (India)',
  'ko': 'Korean',
  'ko-KR': 'Korean (Korea)',
  'kok': 'Konkani',
  'kok-IN': 'Konkani (India)',
  'ky': 'Kyrgyz',
  'ky-KG': 'Kyrgyz (Kyrgyzstan)',
  'lt': 'Lithuanian',
  'lt-LT': 'Lithuanian (Lithuania)',
  'lv': 'Latvian',
  'lv-LV': 'Latvian (Latvia)',
  'mi': 'Maori',
  'mi-NZ': 'Maori (New Zealand)',
  'mk': 'FYRO Macedonian',
  'mk-MK': 'FYRO Macedonian (Former Yugoslav Republic of Macedonia)',
  'mn': 'Mongolian',
  'mn-MN': 'Mongolian (Mongolia)',
  'mr': 'Marathi',
  'mr-IN': 'Marathi (India)',
  'ms': 'Malay',
  'ms-BN': 'Malay (Brunei Darussalam)',
  'ms-MY': 'Malay (Malaysia)',
  'mt': 'Maltese',
  'mt-MT': 'Maltese (Malta)',
  'nb': 'Norwegian (Bokm?l)',
  'nb-NO': 'Norwegian (Bokm?l) (Norway)',
  'nl': 'Dutch',
  'nl-BE': 'Dutch (Belgium)',
  'nl-NL': 'Dutch (Netherlands)',
  'nn-NO': 'Norwegian (Nynorsk) (Norway)',
  'ns': 'Northern Sotho',
  'ns-ZA': 'Northern Sotho (South Africa)',
  'pa': 'Punjabi',
  'pa-IN': 'Punjabi (India)',
  'pl': 'Polish',
  'pl-PL': 'Polish (Poland)',
  'ps': 'Pashto',
  'ps-AR': 'Pashto (Afghanistan)',
  'pt': 'Portuguese',
  'pt-BR': 'Portuguese (Brazil)',
  'pt-PT': 'Portuguese (Portugal)',
  'qu': 'Quechua',
  'qu-BO': 'Quechua (Bolivia)',
  'qu-EC': 'Quechua (Ecuador)',
  'qu-PE': 'Quechua (Peru)',
  'ro': 'Romanian',
  'ro-RO': 'Romanian (Romania)',
  'ru': 'Russian',
  'ru-RU': 'Russian (Russia)',
  'sa': 'Sanskrit',
  'sa-IN': 'Sanskrit (India)',
  'se': 'Sami',
  'se-FI': 'Sami (Finland)',
  'se-NO': 'Sami (Norway)',
  'se-SE': 'Sami (Sweden)',
  'sk': 'Slovak',
  'sk-SK': 'Slovak (Slovakia)',
  'sl': 'Slovenian',
  'sl-SI': 'Slovenian (Slovenia)',
  'sq': 'Albanian',
  'sq-AL': 'Albanian (Albania)',
  'sr-BA': 'Serbian (Latin) (Bosnia and Herzegovina)',
  'sr-Cyrl-BA': 'Serbian (Cyrillic) (Bosnia and Herzegovina)',
  'sr-SP': 'Serbian (Latin) (Serbia and Montenegro)',
  'sr-Cyrl-SP': 'Serbian (Cyrillic) (Serbia and Montenegro)',
  'sv': 'Swedish',
  'sv-FI': 'Swedish (Finland)',
  'sv-SE': 'Swedish (Sweden)',
  'sw': 'Swahili',
  'sw-KE': 'Swahili (Kenya)',
  'syr': 'Syriac',
  'syr-SY': 'Syriac (Syria)',
  'ta': 'Tamil',
  'ta-IN': 'Tamil (India)',
  'te': 'Telugu',
  'te-IN': 'Telugu (India)',
  'th': 'Thai',
  'th-TH': 'Thai (Thailand)',
  'tl': 'Tagalog',
  'tl-PH': 'Tagalog (Philippines)',
  'tn': 'Tswana',
  'tn-ZA': 'Tswana (South Africa)',
  'tr': 'Turkish',
  'tr-TR': 'Turkish (Turkey)',
  'tt': 'Tatar',
  'tt-RU': 'Tatar (Russia)',
  'ts': 'Tsonga',
  'uk': 'Ukrainian',
  'uk-UA': 'Ukrainian (Ukraine)',
  'ur': 'Urdu',
  'ur-PK': 'Urdu (Islamic Republic of Pakistan)',
  'uz': 'Uzbek (Latin)',
  'uz-UZ': 'Uzbek (Latin) (Uzbekistan)',
  'uz-Cyrl-UZ': 'Uzbek (Cyrillic) (Uzbekistan)',
  'vi': 'Vietnamese',
  'vi-VN': 'Vietnamese (Viet Nam)',
  'xh': 'Xhosa',
  'xh-ZA': 'Xhosa (South Africa)',
  'zh': 'Chinese',
  'zh-CN': 'Chinese (S)',
  'zh-HK': 'Chinese (Hong Kong)',
  'zh-MO': 'Chinese (Macau)',
  'zh-SG': 'Chinese (Singapore)',
  'zh-TW': 'Chinese (T)',
  'zu': 'Zulu',
  'zu-ZA': 'Zulu (South Africa)'
}

yang_instruct = """
<?xml version="1.0" encoding="UTF-8" ?>
<i2nsf-cfi-policy
    xmlns="urn:ietf:params:xml:ns:yang:ietf-i2nsf-cons-facing-interface">
    <!-- Policy-level metadata -->
    <name>[Name of the security policy. Must be a unique string.]</name>
    <language>[Language tag per RFC 5646 (e.g., "en-US"). Default: "en-US"]</language>
    <priority-usage>
        <!-- Choose one of:
             "i2nsfcfi:priority-by-order" (default)
             "i2nsfcfi:priority-by-number"
        -->
        priority-by-order
    </priority-usage>
    <resolution-strategy>
        <!-- Choose one of:
             "i2nsfcfi:fmr" (First Matching Rule, default)
             "i2nsfcfi:lmr" (Last Matching Rule)
             "i2nsfcfi:pmre" (Prioritized Matching Rule with Errors)
             "i2nsfcfi:pmrn" (Prioritized Matching Rule with No Errors)
        -->
        fmr
    </resolution-strategy>

    <!-- One or more rules defined using the Event-Condition-Action (ECA) model -->
    <!-- The <rules> element can appear multiple times (it's a YANG list), so repeat the entire <rules>...</rules> block for each new rule. -->
    <rules>
        <name>[Unique name for this rule.]</name>
        <!-- Optional: only present if priority-usage is 'priority-by-number' -->
        <priority>[0-255; higher value = higher priority]</priority>

        <!-- Event: optional triggers (if omitted, rule is always active) -->
        <event>
            <!-- Example: system-event types from ietf-i2nsf-monitoring-interface -->
            <!--
            <system-event>i2nsfmi:config-change</system-event>
            <system-alarm>i2nsfmi:hardware-failure</system-alarm>
            -->
        </event>
        <condition>
            ... condition definitions go here ...
        </condition>
        <action>
            ... action definitions go here ...
        </action>
    </rules>
    <!-- additional <rules> elements as needed -->
    <rules>
        ...
    </rules>

</i2nsf-cfi-policy>
"""

condition_instruct = """
<!-- Condition: all specified sub-conditions must match -->
<condition>
    <!-- Firewall conditions (L2-L4 headers) -->
    <!--
    <firewall>
        <source>[name of user-group or device-group]</source>
        <destination>[name of user-group or device-group]</destination>
        <transport-layer-protocol>i2nsfmi:tcp</transport-layer-protocol>
        <range-port-number>
            <start>80</start>
            <end>80</end>
        </range-port-number>
        <icmp>
            <message>echo</message>
        </icmp>
    </firewall>
    -->

    <!-- DDoS mitigation thresholds -->
    <!--
    <ddos>
        <rate-limit>
            <packet-rate-threshold>1000</packet-rate-threshold>
            <byte-rate-threshold>500000</byte-rate-threshold>
            <flow-rate-threshold>100</flow-rate-threshold>
        </rate-limit>
    </ddos>
    -->

    <!-- Antivirus conditions -->
    <!--
    <anti-virus>
        <profile>/profiles/virus-scan-level2</profile>
        <exception-files>/safe/whitelist.txt</exception-files>
    </anti-virus>
    -->

    <!-- Payload-based detection (references /threat-prevention/payload-content) -->
    <!--
    <payload>
        <content>backdoor-signature-1</content>
    </payload>
    -->

    <!-- URL filtering (references /endpoint-groups/url-group) -->
    <!--
    <url-category>
        <url-name>sns-websites</url-name>
    </url-category>
    -->

    <!-- VoIP/VoCN filtering (references /endpoint-groups/voice-group) -->
    <!--
    <voice>
        <source-id>malicious-callers</source-id>
        <destination-id>employees</destination-id>
        <user-agent>MaliciousBot/1.0</user-agent>
    </voice>
    -->

    <!-- Contextual conditions -->
    <!--
    <context>
        <time>
            <start-date-time>2025-11-28T09:00:00</start-date-time>
            <end-date-time>2025-12-31T18:00:00</end-date-time>
            <period>
                <start-time>09:00:00</start-time>
                <end-time>18:00:00</end-time>
                <day>monday</day>
                <day>tuesday</day>
                <!-- ... -->
            </period>
            <frequency>weekly</frequency>
        </time>
        <application>
            <protocol>i2nsfmi:http</protocol>
        </application>
        <device-type>
            <device>mobile-phone</device>
        </device-type>
        <users>
            <user>
                <id>1001</id>
                <name>alice</name>
            </user>
            <group>
                <id>10</id>
                <name>hr-department</name>
            </group>
        </users>
        <geographic-location>
            <source>
                <country>US</country>
                <region>US-CA</region>
                <city>San Francisco</city>
            </source>
            <destination>
                <country>KR</country>
                <region>KR-11</region>
                <city>Seoul</city>
            </destination>
        </geographic-location>
    </context>
    -->

    <!-- Threat feed reference -->
    <!--
    <threat-feed>
        <name>known-malware-feed</name>
    </threat-feed>
    -->
</condition>
"""

action_instruct = """
<!-- Action: what to do when rule matches -->
<action>
    <primary-action>
        <!-- Required: choose one of:
                i2nsfcfi:pass, i2nsfcfi:drop, i2nsfcfi:reject,
                i2nsfcfi:rate-limit, i2nsfcfi:mirror,
                i2nsfcfi:invoke-signaling, i2nsfcfi:tunnel-encapsulation,
                i2nsfcfi:forwarding, i2nsfcfi:transformation
        -->
        <action>drop</action>
        <!-- Optional: only for rate-limit -->
        <!--
        <limit>1000.00</limit>  <!-- in bytes per second -->
        -->
    </primary-action>
    <secondary-action>
        <!-- Optional: choose one of:
                i2nsfcfi:rule-log, i2nsfcfi:session-log
        -->
        <!-- <log-action>session-log</log-action> -->
    </secondary-action>
</action>
"""

endpoint_instruct = """
<?xml version="1.0" encoding="UTF-8"?>
<endpoint-groups
    xmlns="urn:ietf:params:xml:ns:yang:ietf-i2nsf-cons-facing-interface"
    xmlns:i2nsfmi="urn:ietf:params:xml:ns:yang:ietf-i2nsf-monitoring-interface">

  <!-- User Group: e.g., employees -->
  <user-group>
    <name>[Name of user group, e.g., "employees"]</name>
    <!-- Optional: one or more MAC addresses -->
    <!--
    <mac-address>00:11:22:33:44:55</mac-address>
    -->
    <!-- IPv4 range or prefix -->
    <!--
    <range-ipv4-address>
      <start>192.0.2.10</start>
      <end>192.0.2.20</end>
    </range-ipv4-address>
    -->
    <!-- IPv4 prefix -->
    <!--
    <ipv4-prefix>192.0.2.0/24</ipv4-prefix>
    -->
    <!-- IPv6 range or prefix -->
    <!--
    <range-ipv6-address>
      <start>2001:db8::10</start>
      <end>2001:db8::20</end>
    </range-ipv6-address>
    <ipv6-prefix>2001:db8::/64</ipv6-prefix>
    -->
  </user-group>

  <!-- Device Group: e.g., web servers -->
  <device-group>
    <name>[Name of device group, e.g., "webservers"]</name>
    <!-- IPv4 or IPv6 as above -->
    <!--
    <range-ipv4-address>
      <start>198.51.100.11</start>
      <end>198.51.100.20</end>
    </range-ipv4-address>
    -->
    <!-- Application protocols hosted by these devices -->
    <!--
    <application-protocol>i2nsfmi:http</application-protocol>
    <application-protocol>i2nsfmi:https</application-protocol>
    -->
  </device-group>

  <!-- Location Group: geographic labeling -->
  <location-group>
    <country>[ISO 3166-1 alpha-2 code, e.g., "US"]</country>
    <region>[ISO 3166-2 code, e.g., "US-CA"]</region>
    <city>[City name in English, e.g., "San Francisco"]</city>
    <!-- IPv4 or IPv6 ranges associated with this location -->
    <!--
    <range-ipv4-address>
      <start>203.0.113.0</start>
      <end>203.0.113.255</end>
    </range-ipv4-address>
    -->
  </location-group>

  <!-- URL Group: categorized web destinations -->
  <url-group>
    <name>[Name of URL group, e.g., "sns-websites"]</name>
    <!-- One or more full URIs -->
    <!--
    <url>https://www.socialnetwork1.com/</url>
    <url>https://www.socialnetwork2.net/</url>
    -->
  </url-group>

  <!-- Voice Group: SIP identities for VoIP/VoCN -->
  <voice-group>
    <name>[Name of voice group, e.g., "malicious-callers"]</name>
    <!-- One or more SIP URIs -->
    <!--
    <sip-id>sip:attacker@example.com</sip-id>
    <sip-id>sip:fraud@203.0.113.50</sip-id>
    -->
  </voice-group>

</endpoint-groups>
"""

threat_instruct = """
<?xml version="1.0" encoding="UTF-8"?>
<threat-prevention
    xmlns="urn:ietf:params:xml:ns:yang:ietf-i2nsf-cons-facing-interface">

  <!-- Threat Feed: external threat intelligence -->
  <threat-feed-list>
    <name>[Name of threat feed, e.g., "known-malware-feed"]</name>
    <!-- One or more Indicators of Compromise (IOCs) -->
    <!--
    <ioc>{"indicator": "192.0.2.100", "type": "ip"}</ioc>
    <ioc>{"hash": "a1b2c3...", "type": "file"}</ioc>
    -->
    <!-- Format of the IOC data -->
    <format>
      <!-- Choose one:
           i2nsfcfi:stix
           i2nsfcfi:misp
           i2nsfcfi:openioc
           i2nsfcfi:iodef
      -->
      stix
    </format>
  </threat-feed-list>

  <!-- Payload Content: raw binary threat patterns -->
  <payload-content>
    <name>[Descriptive name, e.g., "backdoor-signature-1"]</name>
    <!-- Optional human-readable description -->
    <!--
    <description>Backdoor command sequence in HTTP payload</description>
    -->
    <contents>
      <content>[Base64-encoded binary pattern, e.g., "UE9TVCAvYmFja2Rvb3I=..."]</content>
      <!-- Optional: max bytes to scan from start of payload -->
      <!--
      <depth>100</depth>
      -->
      <!-- Optional: starting point (choose offset OR distance) -->
      <!--
      <offset>10</offset>
      -->
      <!-- OR -->
      <!--
      <distance>5</distance>  <!-- Only valid for 2nd+ content in ordered list -->
      -->
    </contents>
    <!-- Additional content entries can be added for multi-segment matches -->
    <!--
    <contents>
      <content>...</content>
      <distance>20</distance>
    </contents>
    -->
  </payload-content>

</threat-prevention>
"""

