# MaskDetection-FaceRecognition-COVID19-MonitoringSystem
A python script with GUI interface to detect unmasked individuals and recognise them (known individuals) by their names during COVID-19 pandemic in a workspace.

<h2>About the project</h2>
This python project was created as a submission for a school project during the COVID-19 pandemic. The GUI intentionally contains <i>dumbed down</i> language to make non-technical amongst the staff whom this was presented before, understand the concept better. <br>
The primary logical objectives are as follows:
- 😀 Obtain facial images of persons present in a workspace to train a pre-built face-recognition model.
- 📸 Continously parse a video livestream and to check for faces present frame-by-frame using a caffemodel
- 😷 If any faces detected, check the presence of a mask using pre-trained model.
- 😳 Use the trained face-recognition model to identify the unmasked face and record the name in a locally stored sqlite database.

<h2>How to</h2>
This project is not polished enough to be deployed but the logic can certainly be refined and then extrapolated to handle streams from camera modules via say, a Raspberry Pi. If you wish to just run this project as it is, follow the steps ahead after downlading (&extracting) or cloning this repository.


<h3>1. Virtual Environment</h3>
Open a comand prompt and then navigate to wherever your project is stored.

```
cd <PATH-TO-PROJECT>
```
then type the following to install virtualenv package

```
pip install virtualenv
```
now, you can create a new virtual environment using the following command

```
virtualenv myvirtualenv
```

finally, activate the created virtual environment

```
myvirtualenv\Scripts\activate
```
<h3>2. Install requirements</h3>
In the same terminal, type the following command

```
pip install -requirements.txt
```
make sure you install the same versions as given in the file since I've tested with those versions and open-cv may get cranky at times with others.
<br>
<h3>3. Run</h3>
Run the main_gui.py file. A GUI should open which will contain non-technical jargon, navigate through it step-by-step.

```
py main_hui.py
```
