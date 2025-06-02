import os
import numpy as np
import matplotlib.pyplot as plt
from fastmcp import FastMCP, Image
from mdio import MDIOReader

mcp = FastMCP(
    name="seismic denoising server",
    instructions="""
        This server provides functionalities to denoise seismic data.
        """,
)

@mcp.tool()
async def denoise_svd_with_cutoff(data_path: str, data: str, line_number: int, line_type: str, cutoff_ratio: float = 0.5):
    """
    Denoises a matrix using SVD with a cutoff threshold based on a percentage of the maximum singular value.

    Args:
    data_path: Path to the seismic record file.
    data: Seismic record file, the suffix is usually .sgy or .segy.
    line_number: Inline or crossline number
    line_type: "inline" or "crossline"
    cutoff_ratio: Cutoff ratio used to determine the threshold
                          (threshold = cutoff_ratio * max_singular_value).
    """

    mdio_path = os.path.join(data_path, f"{data.split('.')[0]}.mdio")

    mdio = MDIOReader(mdio_path, return_metadata=True)
    
    inlines = mdio.grid.select_dim("inline").coords
    crosslines = mdio.grid.select_dim("crossline").coords
    times = mdio.grid.select_dim("sample").coords
    std = mdio.stats["std"]

    if line_type == "inline":
        inline_index = mdio.coord_to_index(line_number, dimensions="inline").item()
        _, _, data = mdio[inline_index]
    
    elif line_type == "crossline":
        crossline_index = mdio.coord_to_index(line_number, dimensions="crossline").item()
        _, _, data = mdio[:, crossline_index]

    U, s_orig, Vh = np.linalg.svd(data, full_matrices=False)

    s_max = s_orig[0]
    threshold = cutoff_ratio * s_max

    s_denoised = s_orig.copy()
    s_denoised[s_denoised < threshold] = 0

    num_original_components = len(s_orig)
    num_components_kept = np.sum(s_denoised > 0)

    Sigma_denoised = np.diag(s_denoised)

    data_denoised = U @ Sigma_denoised @ Vh

    data_noise = data - data_denoised

    datasets = [data.T, data_denoised.T, data_noise.T]
    
    titles = [
        f"Original Data",
        f"Denoised Data",
        f"Noise" 
    ]

    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18, 6), sharey=True)

    for i, ax in enumerate(axes):
        current_data = datasets[i]
        current_title = titles[i]

        vmin, vmax = -2 * std, 2 * std
        if line_type == "inline":
            mesh = ax.pcolormesh(crosslines, times, current_data, 
                                vmin=-2*std, vmax=2*std,
                                cmap="seismic", shading='gouraud')
        elif line_type == "crossline":
            mesh = ax.pcolormesh(inlines, times, current_data, 
                                vmin=-2*std, vmax=2*std,
                                cmap="seismic", shading='gouraud')

        ax.invert_yaxis() 
        ax.set_title(current_title)
        
        if line_type == "inline":
            ax.set_xlabel("Crossline Number")
        elif line_type == "crossline":
            ax.set_xlabel("Inline Number")

        if i == 0:
            ax.set_ylabel("TWT (ms)")


        # fig.colorbar(mesh, ax=ax, orientation='vertical')

    plt.tight_layout()
    if line_type == "inline":
        plt.suptitle(f"Seismic Data Comparison (Inline {line_number})", fontsize=16, y=1.02)
        out_file = f"denoised_svd_inline_{line_number}_{cutoff_ratio}.jpg"
    elif line_type == "crossline":
        plt.suptitle(f"Seismic Data Comparison (Crossline {line_number})", fontsize=16, y=1.02)
        out_file = f"denoised_svd_crossline_{line_number}_{cutoff_ratio}.jpg"
    # plt.show()

    plt.savefig(out_file)
    plt.close()
    
    return Image(out_file)


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')