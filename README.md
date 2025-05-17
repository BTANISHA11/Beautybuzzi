# 💄 BEAUTY BUZZ - Face Makeup Editor using PyTorch

**BEAUTY BUZZ** is a revolutionary virtual makeup tool that offers users the ability to try on various makeup styles in real-time. This interactive app makes it easier than ever to experiment with hair and lip colors using deep learning and face parsing techniques.

👉 **[Try the live demo here!](https://beautybuzz.streamlit.app/)**

---

## 🚀 Features

- 🎨 Edit hair and lip colors with realistic effects
- 🧠 Powered by PyTorch & face parsing deep learning models
- 🖼️ Visual comparison of original vs edited look
- 🧪 Experiment with custom RGB color palettes
- 🖥️ Live demo using Streamlit interface

---

## 🖥️ Run the Project Locally

```bash
streamlit run app.py
````

# face-makeup.PyTorch
Lip and hair color editor using face parsing maps.

### Command to run the project:
    streamlit run app.py

<table>

<tr>
<th>&nbsp;</th>
<th>Hair</th>
<th>Lip</th>
</tr>

<!-- Line 1: Original Input -->
<tr>
<td><em>Original Input</em></td>
<td><img src="makeup/116_ori.png" height="256" width="256" alt="Original Input"></td>
<td><img src="makeup/116_lip_ori.png" height="256" width="256" alt="Original Input"></td>
</tr>

<!-- Line 2: Color -->
<tr>
<td >Color</td>
<td><img src="makeup/116_0.png" height="256" width="256" alt="Color"></td>
<td><img src="makeup/116_6.png" height="256" width="256" alt="Color"></td>
</tr>

<!-- Line 3: Color -->
<tr>
<td>Color</td>
<td><img src="makeup/116_1.png" height="256" width="256" alt="Color"></td>
<td><img src="makeup/116_3.png" height="256" width="256" alt="Color"></td>
</tr>

<!-- Line 4: Color -->
<tr>
<td>Color</td>
<td><img src="makeup/116_2.png" height="256" width="256" alt="Color"></td>
<td><img src="makeup/116_4.png" height="256" width="256" alt="Color"></td>
</tr>

</table>

### Using PyTorch 1.0 and python 3.x

## Demo
Change hair and lip color:
```Shell
python makeup.py --img-path imgs/116.jpg
```
### Try to use other colors:
Change the color list in **makeup.py**(line 83)
```
colors = [[230, 50, 20], [20, 70, 180], [20, 70, 180]]
```
### Train face parsing model (Optional)
Follow this repo [zllrunning/face-parsing.PyTorch](https://github.com/zllrunning/face-parsing.PyTorch)
