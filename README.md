# translator

- Translate markdown files into japanese, by using [`doctran`](https://github.com/psychic-api/doctran).
- Generally, the file format is preserved before and after translation.
- Environment value `OPENAI_API_KEY` is read from `.env` by utilizing [`pipenv` function](https://pipenv-ja.readthedocs.io/ja/translate-ja/advanced.html#support-for-environment-variables).

```sh
./main.py [--throttle 3] --dir $target_dir [-v]
```
