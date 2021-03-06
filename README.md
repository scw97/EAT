# EXPRESSO ANALYSIS TOOLBOX (EAT) #

**E**xpresso **A**nalysis **T**oolbox (EAT) is a Python toolbox for analyzing data from Expresso behavioral assays, in which the food consumption of individual *Drosophila* is monitored on the nanoliter scale (described in [Yapici et al., 2016](https://doi.org/10.1016/j.cell.2016.02.061). EAT expands on the original Expresso assay by combining high-resolution food intake measurements with motion tracking, allowing a multi-faceted analysis of *Drosophila* feeding and foraging behavior. For more information, see our manuscript: [to be determined](http://yapicilab.com/research-projects.html).

### Expresso Hardware and Firmware ###

EAT is designed to be used for analyzing data from Expresso behavioral assays. The resources listed below can be used to build the apparatus for Expresso experiments and collect data during Expresso experiments. Additional details can be found in the Methods section of our manuscript: [to be determined](http://yapicilab.com/research-projects.html).

* [Open source plans for Expresso sensor banks](http://public.iorodeo.com/docs/expresso/hardware_design_files.html)

* [Source code for Expresso data acquisition software](http://public.iorodeo.com/docs/expresso/device_software.html)

### EAT Installation ###

EAT can be run on Windows, Linux, or MacOS. We recommend an **Anaconda environment** based installation, as it provides the easiest route to get things running, but the installation process can be adapted to other Python distributions as needed. The steps to install EAT using an Anaconda environment are described below:

1. **Install Anaconda** [File download](https://www.anaconda.com/products/individual) | [Installation guide](https://docs.anaconda.com/anaconda/install/) 

2. **Download EAT code** [GitHub repository](https://github.com/scw97/EAT)

3. **Create EAT Anaconda environment** In the Anaconda terminal (or Unix terminal), navigate to the root folder of the EAT code and run the following:
	* **`conda env create --file eat.yaml`**
	* **`conda activate eat`**

4. **Run EAT** Choose to run EAT from either the Anaconda terminal or Spyder.
	* (terminal) In the same terminal, run:
		* **`cd src`**
		* **`python visual_expresso_gui_main.py`**
	* (Spyder) In the same terminal, run:
		* **`Spyder`** 
		* In Spyder, open `visual_expresso_gui_main.py` and run

If all installation steps proceeded correctly, the final step (#4) should open the main EAT GUI window. For subsequent usage of the EAT code after following the installation instructions above, make sure to run files from the EAT Anaconda environment, either via the command line using `conda activate eat` or via the settings in your Python IDE. For additional questions/comments please contact us at either [scw97@cornell.edu](mailto:scw97@cornell.edu) or [ny96@cornell.edu](mailto:ny96@cornell.edu). 

### Usage ###

The main tools from EAT are three GUI interfaces which deal with pre-processing, processing, and post-processing data from Visual Expresso behavioral assays. These three are briefly described below:

* **`crop_and_save_gui.py`** is used to crop and save videos taken during Visual Expresso experiments. The cropped videos assist in data sorting and computation time for future analyses, and are thus a vital part of the analysis pipeline.
* **`visual_expresso_gui_main.py`** is the main GUI interfact use to analyze Expresso data. It is used to perform meal bout detection, video tracking, plotting data, and saving analysis results.
* **`post_processing_gui.py`** is used with analysis summary files generated by `visual_expresso_gui_main.py` to perform groupwise comparisons both via generating plots and performing hypothesis testing.

For a more detailed walkthrough of EAT, see our [User Guide](https://github.com/scw97/EAT/blob/master/demo/USER_GUIDE.md).


