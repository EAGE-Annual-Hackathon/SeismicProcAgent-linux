# SeismicProcAgent-linux
The open source basic demo for seismic data process AI agent using MCP and LLMs. Suitable for running on Linux servers (command line interaction).

## Quick Start
### Environment Requirements
* `Python`: 3.10+
* `node`: v22.16.0+
* `npm/npx`: 10.9.2+

SeismicProcAgent is developed in Python. To ensure a smooth setup process, we recommend using [`uv`](https://docs.astral.sh/uv/getting-started/installation/) to manage the Python environment and dependencies. In the terminal we execute:
```
# MacOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
Then download and install [`Node.js`](https://nodejs.org/en/download/) according to your operating system. Be sure to restart your terminal afterwards to ensure the `uv/npm/npx` command is recognized.

### Installation
```
# Clone the repository
git clone https://github.com/JiahuaZhao/SeismicProcAgent.git
cd SeismicProcAgent

# Install dependencies
uv sync
```
Then download and install [`Claude for Desktop`](https://claude.ai/download) according to your operating system, we will configure it next.

### Configuration
Please refer to the configuration process shown in the MCP document: https://modelcontextprotocol.io/quickstart/user, and add the following content when configuring `claude_desktop_config.json`:
```
# MacOS/Linux
{
  "mcpServers": {
      "sequential-thinking": {
          "command": "npx",
          "args": [
              "-y",
              "@modelcontextprotocol/server-sequential-thinking"
          ]
      },
      "filesystem": {
          "command": "npx",
          "args": [
              "-y",
              "@modelcontextprotocol/server-filesystem",
              "/Your_Local_Path/SeismicProcAgent"
          ]
      },
      "seismic_basic_tools": {
          "command": "uv",
          "args": [
              "--directory",
              "/Your_Local_Path/SeismicProcAgent",
              "run",
              "basic_tools.py"
          ]
      },
      "seismic_attributes": {
          "command": "uv",
          "args": [
              "--directory",
              "/Your_Local_Path/SeismicProcAgent",
              "run",
              "seismic_attributes.py"
          ]
      },
      "seismic_denoising": {
          "command": "uv",
          "args": [
              "--directory",
              "/Your_Local_Path/SeismicProcAgent",
              "run",
              "denoising.py"
          ]
      },
      "seismic_ai_tools": {
          "command": "uv",
          "args": [
              "--directory",
              "/Your_Local_Path/SeismicProcAgent",  
              "run",
              "ai_tools.py"
          ]
      }
  }
}
```
```
# Windows
{
  "mcpServers": {
      "sequential-thinking": {
          "command": "npx",
          "args": [
              "-y",
              "@modelcontextprotocol/server-sequential-thinking"
          ]
      },
      "filesystem": {
          "command": "npx",
          "args": [
              "-y",
              "@modelcontextprotocol/server-filesystem",
              "C:\\Users\\Your_Local_Path\\SeismicProcAgent"
          ]
      },
      "seismic_basic_tools": {
          "command": "uv",
          "args": [
              "--directory",
              "C:\\Users\\Your_Local_Path\\SeismicProcAgent",
              "run",
              "basic_tools.py"
          ]
      },
      "seismic_attributes": {
          "command": "uv",
          "args": [
              "--directory",
              "C:\\Users\\Your_Local_Path\\SeismicProcAgent",
              "run",
              "seismic_attributes.py"
          ]
      },
      "seismic_denoising": {
          "command": "uv",
          "args": [
              "--directory",
              "C:\\Users\\Your_Local_Path\\SeismicProcAgent",
              "run",
              "denoising.py"
          ]
      },
      "seismic_ai_tools": {
          "command": "uv",
          "args": [
              "--directory",
              "C:\\Users\\Your_Local_Path\\SeismicProcAgent",  
              "run",
              "ai_tools.py"
          ]
      }
  }
}
```
After updating your configuration file, you need to restart Claude for Desktop. Upon restarting, you should see a slider icon in the bottom left corner of the input box. After clicking on the slider icon, you should see the tools. At the same time, you can click on the tools to choose whether to use the tools (it is recommended to turn off `sequentialthinking` for the first time).

### Let’s have fun
The following examples (Chat Prompts) demonstrate the capabilities of SeismicProcAgent:
### Primary
* ##### Seismic Data Overview
```
"Show me the ebdic of the seismic data: /Your_Local_Path/Dutch_Government_F3_entire_8bit_seismic.segy."
```
* ##### Seismic Data Visualization
```
"Please plot the image of inline 400 for /Your_Local_Path/Dutch_Government_F3_entire_8bit_seismic.segy."
```
* ##### Seismic Attributes
```
"Please plot the envelope image of inline 400 for /Your_Local_Path/Dutch_Government_F3_entire_8bit_seismic.segy."
```
* ##### Seismic Data Denoising
```
"Please run a SVD denoise on crossline 500 using a cut off of 0.3 for /Your_Local_Path/Dutch_Government_F3_entire_8bit_seismic.segy."
```
* ##### Seismic Data Denoising (AI)
```
"Please use the AI ​​method to process the data with inline = 400 for /Your_Local_Path/Dutch_Government_F3_entire_8bit_seismic.segy and show the results."
```
### Advance
* ##### DeepProcess (sequential-thinking)
> [!NOTE]
> This function still under testing, need to enable the `sequential-thinking` tool, and consume more tokens. 
```
"Please help me process and analyze the seismic data: /Your_Local_Path/Dutch_Government_F3_entire_8bit_seismic.segy and show the results, from a 2D and 3D perspective, interpret the results generated by the processing, and finally organize the results into a html document and save it in local."
```
