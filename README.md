# SeismicProcAgent-linux
The open source basic demo for seismic data process AI agent using MCP and LLMs. Suitable for running on Linux servers (command line interaction), or private deployment. Built in the Hackathon hosted at the EAGE Annual 2025 in Toulouse, France.

## Quick Start
### Environment Requirements
* `Python`: 3.10+
* `node`: v18.19.1+
* `npm/npx`: 9.2.0+

SeismicProcAgent is developed in Python. To ensure a smooth setup process, we recommend using [`uv`](https://docs.astral.sh/uv/getting-started/installation/) to manage the Python environment and dependencies. In the terminal we execute:
```
url -LsSf https://astral.sh/uv/install.sh | sh

Or

wget -qO uv.tar.gz https://github.com/astral-sh/uv/releases/latest/download/uv-x86_64-unknown-linux-gnu.tar.gz
sudo tar xf uv.tar.gz --strip-components=1 -C /usr/local/bin uv-x86_64-unknown-linux-gnu/uv
```
Then download and install [`Node.js`](https://nodejs.org/en/download/):
```
sudo apt update
sudo apt install nodejs npm
```

### Installation
```
# Clone the repository
git clone https://github.com/JiahuaZhao/SeismicProcAgent-linux.git
mv SeismicProcAgent-linux SeismicProcAgent && cd SeismicProcAgent

# Install dependencies
uv sync
```

### Configuration
#### Local execution (Ollama)
First, make sure that Ollama is installed on your local linux server:
```
ollama -v 
```
If there is no Ollama:
```
curl -fsSL https://ollama.com/install.sh | sh
```

If your linux server has a GPU, you can visit: https://ollama.com/search ​​to obtain Ollama models, and then you can run the large language model locally (multimodal models are recommended):
```
# GPU memory is more than 8 GB
ollama pull qwen3:8b
```
Then you can modify the `.env` and change the `OLLAMA_MODEL_NAME` to the model name you actually download:
```
# For example
BASE_URL=http://localhost:11434/v1
API_KEY=ollama
MODEL_NAME=qwen3:8b
```
#### Calling the APIs
If the server does not have any GPUs, or you do not want to run local LLMs, we can also call the APIs to use the LLMs. Take the OpenAI API format () as an example, you also need to modify the configuration in `.env`:
```
BASE_URL=https://integrate.api.nvidia.com/v1/chat/completions
NVIDIA_API_KEY=Your API key
MODEL_NAME=qwen/qwen3-235b-a22b
```
Model resources are supported by NVIDIA: https://build.nvidia.com/models, or:

```
BASE_URL=https://api.openai.com/v1
OPENAI_API_KEY=Your API key
MODEL_NAME=gpt-4.1-nano
```

### Specific Functions
* #### Overview:
    * overview: 
        * Overview of the seismic data (.sgy and .segy).
* #### Data format conversion:
    * segy2mdio:
        * Convert a SEGY file to MDIO format.
    * mdio2segy:
        * Convert MDIO file to SEGY file.
* #### Visualization:
    * mdio_plot_inline:
        * Read MDIO file and plot the inline.
    * mdio_plot_crossline:
        * Read MDIO file and plot the crossline.
    * mdio_plot_time: 
        * Read MDIO file and plot the crossline.
    * frequency_spectrum_2d:
        * Calculate the frequency spectrum of a 2D seismic data.
    * frequency_spectrum_3d:
        * Calculate the frequency spectrum of a 3D seismic data.
* #### Seismic attributes:
    * sliceAttribute:
        * Computing attribute of a 3D seismic cube, output a 2D attribute slice.
        * Attribute classes: Amplitude, CompleTrace, DipAzm (dip and azimuth), EdgeDetection (edge detection).
            * Each class has different attribute types, as follows:
                * For class 'Amplitude', attributes are:
                    * 'fder': first derivative
                    * 'sder': second derivative
                    * 'rms': rms of trace value (e.g. amplitude)
                    * 'gradmag': gradient magnitude using Gaussian operator
                    * 'reflin': reflection intensity
                * For class 'CompleTrace', attributes are: 
                    * 'enve': envelope
                    * 'inphase': instantaneous phase 
                    * 'cosphase': cosine instantaneous phase 
                    * 'ampcontrast': relative amplitude contrast
                    * 'ampacc': amplitude acceleration
                    * 'infreq': instantaneous frequency 
                    * 'inband': instantaneous bandwidth
                    * 'domfreq': dominant frequency 
                    * 'freqcontrast': frequency change 
                    * 'sweet': sweetness 
                    * 'quality': quality factor 
                    * 'resphase': response phase 
                    * 'resfreq': response frequency 
                    * 'resamp': response amplitude 
                    * 'apolar': apparent polarity
                * For class 'DipAzm', attributes are: 
                    * 'dipgrad': gradient dips from inline, crossline, and z-gradients 
                    * 'gst': the gradient structure tensors (GST), inner product of 
                        gradients.
                    * 'gstdip2d': 2D gradient dips from GST
                    * 'gstdip3d': 3D gradient dips from GST
                    * 'gstazm3d': 3D azimuth from GST
                * For class 'EdgeDetection', attributes are:
                    * 'semblance': semblance
                    * 'gstdisc': discontinuity from eigenvalues of GST
                    * 'eigen': multi-trace semblance from 3D seismic incorporating the 
                                analytic trace
                    * 'chaos': multi-trace chaos from 3D seismic
                    * 'curv': volume curvature from 3D seismic dips

### Let’s have fun
First we need to run the Python scripts:
```
source .venv/bin/activate

# Ollama
python main_ollama.py

# APIs
python main_openai.py
```
Then interactively operate, the following examples (Chat Prompts) demonstrate the capabilities of SeismicProcAgent-linux:
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
