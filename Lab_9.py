import imghdr
from tkinter import * 
from tkinter import ttk
import os
import sys
import ctypes

from requests import request
import requests
from pokeapi import get_pokemon_image_url, get_pokemon_list

def main():
    
    script_dir = sys.path[0]
    images_dir = os.path.join(script_dir,'images')
    if not os.path.isdir(images_dir):
        os.makedirs(images_dir)

    root =Tk()
    root.title('Pokemon Image Viewer')
    app_id = 'COMP593.ImageViewer'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    root.iconbitmap(os.path.join(script_dir,'PokeBall.ico'))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.geometry('600x600  ')

    frm = ttk.Frame(root)
    frm.grid(sticky=(N,S,E,W))  
    frm.columnconfigure(0, weight=1)
    frm.rowconfigure(0, weight=1)

    img_pokemon = PhotoImage(file=os.path.join(script_dir,'Pokemon.png'))
    lbl_image = Label(frm, image=img_pokemon)
    lbl_image.grid(row=0, column=0)

    pokemon_list = get_pokemon_list(limit= 1000)
    pokemon_list.sort()
    cbo_pokemon_sel = ttk.Combobox(frm, values= pokemon_list, state='readonly')
    cbo_pokemon_sel.set('Select Pokemon')
    cbo_pokemon_sel.grid(row=1, column=0)

    def handle_cbo_pokemon_sel(event):
        
        pokemon_name = cbo_pokemon_sel.get()
        image_url = get_pokemon_image_url(pokemon_name)
        image_path = os.path.join(images_dir, pokemon_name + '.png')
        if download_image_from_url(image_url, image_path):
            img_pokemon['file'] = image_path
            btn_set_desktop.state(['!disabled'])
    cbo_pokemon_sel.bind('<<ComboboxSelected>>', handle_cbo_pokemon_sel)

    def btn_set_desktop_click():
        pokemon_name = cbo_pokemon_sel.get()
        image_path = os.path.join(images_dir, pokemon_name + '.png')
        set_dektop_background_image(image_path)

    btn_set_desktop = ttk.Button(frm, text= 'Set as the Desktop Image', command= btn_set_desktop_click)
    btn_set_desktop.state(['disabled'])
    btn_set_desktop.grid(row=2, column=0, padx=10, pady=10)

    root.mainloop()

def set_dektop_background_image(path):

    try:
         ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)

    except:
        print("Error setting desktop background Image")

def download_image_from_url(url,path):
    
    if os.path.isfile(path):
        return path

    resp_msg =requests.get(url)
    if resp_msg.status_code == 200:
        try:
            img_data = resp_msg.content
            with open(path, 'wb') as fp:
                fp.write(img_data)
            return path
        except:
            return
    
    else:
        print('Failed to get Pokemon list.')
        print('Response code:', resp_msg.status_code)
        print(resp_msg.text)
main() 