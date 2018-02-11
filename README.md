# DankQWOPRunner
If dank is what you looking for, you've come to the right place. This dank ass runner will learn to run using a genetic algorithm coded by two plonks. GG NO RE. Usain bolt learnt to run from years of observing this dank ass runner.


## Installing MSS (Multiple Screen Shots)
MSS is responsible for taking screenshots of QWOP.

```sh 
sudo -H pip install --upgrade mss
```

## Installing pynput

* pip install `pynput`

_(Optional)_ If you are using PyCharm set up `pynput` as follows:

* File -> Settings -> Project: DankQWOPRunner -> Project Interpreter
* Click the green '+'
* Search for `pynput`
* Click install package

## Installing Tesseract
Python uses `tesseract` by spawning a subprocess of `tesseract` within your executing program. 
So we need to install `tesseract` first and then a python wrapper around that called `pytesseract`.

As I understand it, `pytesseract` needs Python Image Library (PIL) as a dependency.
On Ubuntu 16.04, it was installed by default as `pillow`.
Also, `pytesseract` pulls `pillow` in as a dependency; but if you get any dependency issues, then you should just install `pillow`.

### Ubuntu:
```sh
sudo apt install tesseract-ocr
sudo -H pip install pytesseract
```
