#! /usr/bin/python3.10

"""
Author: Henri Nuortila

Graphical user interface for OpenAI's text to speech model.
Built with PySimpleGUI.
"""


import os
import textwrap

import api_call

import PySimpleGUI as sg
import openai

sg.theme("Topanga")

VOICES = {
    "Alloy":"alloy", 
    "Echo":"echo", 
    "Fable":"fable", 
    "Onyx":"onyx", 
    "Nova":"nova", 
    "Shimmer":"shimmer"}

def want_to_overwrite(path):
    path_text = sg.Text(text = path,
                        text_color="White",
                        pad=20)
    explanation = sg.Text(f"A file with the same name was found. \
Do you want to overwrite it?")
    yes_button = sg.Button("YES", key="yes",
                           size=(4, 2),
                           pad=15)
    no_button = sg.Button("NO", key="no",
                          size=(4, 2),
                          pad=15)

    window = sg.Window(title="Do you want to overwrite?",
                       layout=[[path_text],
                               [explanation],
                               [yes_button, no_button]],
                       font=("Lato", 18),
                       element_justification=("c"))
    while True:
        event, _ = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == "yes":
            window.close()
            return True
        elif event == "no":
            window.close()
            return False
    
    window.close()
    return None
    

def handle_call(prompt, voice, api_key, target_directory, save_name) -> None:
    """ Executes api call with error handling."""
                
    try:
        api_call.tts_api_call(prompt=prompt,
                          voice=voice,
                          api_key=api_key,
                          file_folder=target_directory,
                          file_name=save_name)
    except openai.APIConnectionError as con_er:
        print(con_er.body)
        msg = f"{con_er.message} This will also happen, if you did \
not send an api-key at all."
        display_error(msg)
    except openai.AuthenticationError as auth_er:
        msg = auth_er.body['message']
        display_error(msg)
    except UnicodeEncodeError as ö_er:
        msg = f"Error: You might have used a character \
outside of the English aplhabet in your api-key. {ö_er}"
        display_error(msg)
    except openai.BadRequestError as empt_er:
        msg = empt_er.body['message']
        display_error(f"Error: You probably did not send a prompt. {msg}")
    except:
        print("Oopsie daisie, Houston: 'We have a problem!")
        msg = "An unexpected error happened and I am about to crash! \
Please contact the author."
        display_error(msg, is_bug=True)
    finally:
        api_call.tts_api_call(prompt=prompt,
                              voice=voice,
                              api_key=api_key,
                              file_folder=target_directory,
                              file_name=save_name)


def display_error(error_message, is_bug=False):
    if is_bug:
        warpped_error = textwrap.fill(error_message, 50)

        error_text = sg.Text(f"{warpped_error}", pad=40, expand_y=True)
        close_button = sg.Button("Close", key="close",
                                 size=(1, 1),
                                 pad=15,
                                 image_filename="./pictures/bug_button.png",
                                 image_size=(100, 100),
                                 border_width=3,
                                 mouseover_colors=("Red"))
        error_window = sg.Window(error_text,
                                 layout=[[error_text, close_button]],
                                 font=("Lato", 18))
        while True:
            event, values = error_window.read()
            if event == 'close' or event == sg.WIN_CLOSED:
                break
    else:
        warpped_error = textwrap.fill(error_message, 50)

        error_text = sg.Text(f"{warpped_error}", pad=40, expand_y=True)
        close_button = sg.Button("Close", key="close", size=(5, 3), pad=15)
        error_window = sg.Window(error_text,
                                 layout=[[error_text, close_button]],
                                 font=("Lato", 18))
        
        while True:
            event, _ = error_window.read()
            if event == 'close' or event == sg.WIN_CLOSED:
                break

    error_window.close()


def main_menu():
    voices_list = [i for i in VOICES.keys()]
    voice_select = sg.DropDown(values=voices_list,
                               key="voice_select",
                               default_value="Echo")
    
    select_voice_text = sg.Text("SELECT VOICE", pad=15)
    api_prompt = sg.Text(text="API-KEY",
                         tooltip="Insert your openai API-key here")

    api_input = sg.Input(tooltip="API-KEY",
                         pad=10,
                         key="api")
    prompt_text = sg.Text(text="Text to process:",
                          pad=15)
    prompt_input = sg.Multiline(expand_x=True,
                                expand_y=True,
                                size=(10, 10),
                                key="prompt")

    browse_text = sg.Text("Save to folder:",
                          pad=15)
    browse_button = sg.FolderBrowse("Browse",
                                    key="folder",
                                    tooltip="Select target directory")
    submit_button = sg.Button("CONVERT",
                              tooltip="All it takes is one click :)",
                              key="convert",
                              size=(15, 3),
                              pad=15)
    quit_button = sg.Button(button_text="QUIT",
                            key="quit",
                            tooltip="Quit program",
                            pad=40,
                            mouseover_colors="Red",
                            size=(5, 2))
    
    filename_text = sg.Text("Filename")
    default_filename = "tts_audio"
    filename_input = sg.Input(default_filename,
                              text_color="White",
                              key="name",
                              pad=5)

    layout = [
        [api_input, api_prompt],
        [voice_select, select_voice_text],
        [prompt_text],
        [prompt_input],
        [browse_text, browse_button],
        [filename_text, filename_input],
        [submit_button],
        [quit_button]
              ]

    window = sg.Window("GUI TEST",
                       layout=layout,
                       font=("Lato", 18),
                       element_justification="c",
                       relative_location=(0, -100)
                       )

    press_count = 0
    filename = default_filename
    while True:
        event, values = window.read(timeout=200)
        if event == sg.WIN_CLOSED or event == "quit":
            break
        elif event == "convert":
            new_name = values['name']
            save_name = f"{new_name}"

            if values['folder']:
                print("This is True")
                target_directory = values['folder']
            else:
                if not os.path.exists("./results"):
                    os.mkdir("./results")
                    print("created the results folder")
                target_directory = "./results"

            prompt = values['prompt']
            voice = VOICES[values['voice_select']]
            api_key = values['api']
            full_path = f"{target_directory}/{save_name}.mp3"
            print(full_path)
            if os.path.exists(full_path):
                if want_to_overwrite(full_path):
                    print("Execute overwrite")
                    handle_call(prompt=prompt,
                            voice=voice,
                            api_key=api_key,
                            target_directory=target_directory,
                            save_name=save_name)
                else:
                    print("No_overwrite!")
            else:
                print(full_path)
                handle_call(prompt=prompt,
                            voice=voice,
                            api_key=api_key,
                            target_directory=target_directory,
                            save_name=save_name)
                
            """ This feature updates the filename with an increasing
            number to make iterations with a similar filename faster. """
                
            # First 'convert' button press
            if press_count == 0:
                # We could plus one it, but this is set to explicitly
                # as the first press
                press_count = 1
                next_name = f"{new_name}_{press_count}"
                window['name'].update(next_name)
                filename = next_name
            # 'Other times 'convert' is pressed
            elif press_count >= 1:
                count_len = len(str(press_count))
                name_no_num = new_name[:-count_len]
                press_count += 1
                next_name = f"{name_no_num}{press_count}"
                test_last = f"{name_no_num}{press_count - 1}"
                
                # User did not change the name
                if filename == test_last:
                    window['name'].update(next_name)
                    filename = next_name
                # User changed the name
                else:
                    # Start new filename count
                    press_count = 1
                    next_name = f"{new_name}_{press_count}"
                    window['name'].update(next_name)
                    filename = next_name
    window.close()

if __name__ == "__main__":
    main_menu()