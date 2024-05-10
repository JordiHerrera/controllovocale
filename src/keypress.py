import pyautogui
action = 'paste'
def case_actions(action,distance = 75):
    if action == 'copy':
        pyautogui.hotkey('ctrl','c')
    elif action == 'paste':
        pyautogui.hotkey('ctrl','v')
    elif action == 'cut':
        pyautogui.hotkey('ctrl','x')
    elif action == 'undo':
        pyautogui.hotkey('ctrl','z')
    elif action == 'redo':
        pyautogui.hotkey('ctrl','y')
    elif action == 'up_mouse':
        pyautogui.moveRel(xOffset=0, yOffset=-distance, duration=0.15)
    elif action == 'down_mouse':
        pyautogui.moveRel(xOffset=0, yOffset=distance, duration=0.15)
    elif action == 'rigth':
        pyautogui.moveRel(xOffset=distance, yOffset=0, duration=0.15)
    elif action == 'left':
        pyautogui.moveRel(xOffset=-distance, yOffset=0, duration=0.15)
    elif action == 'click':
        pyautogui.click()
    elif action == 'double click':
        pyautogui.doubleClick()
    else:
        print('Queseso')
        return -1
    return 1


