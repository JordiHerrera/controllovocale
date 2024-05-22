import pyautogui

actions_list = [['escribir', 'abajo', 'abajo', 'abajo', 'arriba', 'arriba']]

def case_actions(actions, distance=75):
    for action in actions:
        if not isinstance(action, list):
            if action == 'copiar':
                pyautogui.hotkey('ctrl', 'c')
            elif action == 'cerrar':
                pyautogui.hotkey('alt', 'f4')
            elif action == 'pegar':
                pyautogui.hotkey('ctrl', 'v')
            elif action == 'cortar':
                pyautogui.hotkey('ctrl', 'x')
            elif action == 'deshacer':
                pyautogui.hotkey('ctrl', 'z')
            elif action == 'rehacer':
                pyautogui.hotkey('ctrl', 'y')
            elif action == 'clic':
                pyautogui.click()
            elif action == 'doble':
                pyautogui.doubleClick()
            else:
                print('Queseso')
                return -1
        else:
            for i in range(1, len(action)):
                print(i)
                if action[0] == 'mover':
                    if action[i] == 'arriba':
                        pyautogui.moveRel(xOffset=0, yOffset=-distance, duration=0.15)
                    elif action[i] == 'abajo':
                        pyautogui.moveRel(xOffset=0, yOffset=distance, duration=0.15)
                    elif action[i] == 'derecha':
                        pyautogui.moveRel(xOffset=distance, yOffset=0, duration=0.15)
                    elif action[i] == 'izquierda':
                        pyautogui.moveRel(xOffset=-distance, yOffset=0, duration=0.15)
                if action[0] == 'clic':
                    if action[i] == 'derecha':
                        pyautogui.rightClick()
                    if action[i] == 'izquierda':
                        pyautogui.click()
                    if action[i] == 'central':
                        pyautogui.middleClick()
                if action[0] == 'escribir':
                    pyautogui.write(action[i])
                    pyautogui.press('space')

    return 1

case_actions(actions_list)
