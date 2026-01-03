import { NextResponse } from 'next/server';
import { execFile } from 'child_process';
import { promisify } from 'util';
import path from 'path';
import fs from 'fs/promises';

const execFileAsync = promisify(execFile);
export const runtime = 'nodejs';

export async function POST(req: Request) {
  try {
    const { intent } = await req.json();

    const uiRoot = process.cwd(); // ~/dmins/packages/ui
    const backendRoot = path.join(uiRoot, '..', '..', 'llm_backend');

    const scriptPath = path.join(backendRoot, 'generate.py');
    const xmlPath = path.join(backendRoot, 'generated_policy.xml');

    const { stdout, stderr } = await execFileAsync('python3', [scriptPath, intent], {
      cwd: backendRoot,
    });

    if (stderr) {
      console.error('generate.py stderr:', stderr);
    }

    const xml = await fs.readFile(xmlPath, 'utf-8');

    return NextResponse.json({
      output: xml,
      log: stdout,
    });
  } catch (err) {
    console.error(err);
    return NextResponse.json(
      { error: 'failed to run generator' },
      { status: 500 },
    );
  }
}
