For osx or linux.

#### Setup
- Install requirements by running command on console.
    ```pip install -r requirements.txt```
- Setup google [service account key](https://cloud.google.com/translate/docs/reference/libraries#client-libraries-usage-python).
- Export google service account key variable on console.
    ```export GOOGLE_APPLICATION_CREDENTIALS="/home/user/Downloads/service-account-file.json"```


#### To run:
- Use command ```python main.py```
- Input file path like ```/Users/myname/work/sample/wiki.po```
- Input language for example `ur` for `urdu` and `en` for `english`

```python
(ven) amir$ python main.py
Please input file or folder full path: /Users/source/sample # whole folder
Please input target language i.e en for english: ur  # language code
```

#### Useful links
- https://cloud.google.com/translate/quotas
- http://polib.readthedocs.io/en/latest/quickstart.html#creating-po-catalogs-from-scratch
- https://cloud.google.com/translate/docs/reference/libraries#client-libraries-resources-go
