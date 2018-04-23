#### Introduction:
This tool uses google translator to translate msgid(s) in django PO file. You can supply a target language 
and folder or **.PO** file absolute location in the input and tool will provide you translated file(s) 
in **dest** folder. 

I used this tool to translate [edX](https://github.com/edx/edx-platform/) strings in urdu language. 

- Python 2 is used.
- Tutorial for osx or linux only.

#### Setup
- Install requirements by running command on console.
    
    ```pip install -r requirements.txt```
- Setup google [service account key](https://cloud.google.com/translate/docs/reference/libraries#client-libraries-usage-python).
- Enable google translator api on your project from google cloud console.
- Export google service account key variable on console.
 
    ```export GOOGLE_APPLICATION_CREDENTIALS="/home/user/Downloads/service-account-file.json"```


#### To run:
- Use command `python main.py`
- Input file path like `sample/wiki.po` or folder path like `sample`
- Input language or languages for example `ur` for `urdu` and `en` for `english`.
- For single language input like: `ur`
- For multi language input like: `zh-CN,ur,ar`. You can add as much languages you want.
 Add comma to separate them without spaces.
- You can find list of supported languages [here](https://ctrlq.org/code/19899-google-translate-languages).

```python
(ven) amir$ python main.py
Please input file or folder full path: sample  # whole folder
Please input target language(s) comma separated i.e en for english: ur,ar  # language codes urdu, arabic
```

#### Useful links
- https://cloud.google.com/translate/quotas
- http://polib.readthedocs.io/en/latest/quickstart.html#creating-po-catalogs-from-scratch
- https://cloud.google.com/translate/docs/reference/libraries#client-libraries-resources-go
 