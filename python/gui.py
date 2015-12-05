#!/usr/bin/env python

import Tkinter


if __name__ == '__main__':
	root = Tkinter.Tk()

	label = Tkinter.Label(root, text="hello world!")
	label.pack()

	btn = Tkinter.Button(root, text="Press me!!!", command=root.quit, bg='red', fg='white')
	btn.pack(fill=Tkinter.X, expand=1)

	Tkinter.mainloop()