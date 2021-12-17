import pyautogui
import time
import os
import albumentations as A
import cv2

#P(x = 766, y = 1046)

def screenshots_maker(dir, img_name, program_icon_x, program_icon_y):
    pyautogui.click(program_icon_x, program_icon_y)
    pyautogui.hotkey('ctrl', 't')
    for constellation_name in os.listdir(dir):
        pyautogui.hotkey('ctrl', 'f')
        pyautogui.click(711, 462, clicks=2)
        pyautogui.press('backspace')
        pyautogui.typewrite(constellation_name)
        pyautogui.typewrite(["enter"])

        #delay
        time.sleep(4)
        myScreenshot = pyautogui.screenshot()
        myScreenshot.save(f"{dir}/{constellation_name}/" + img_name)
        print(f"{constellation_name} - screenshots taken")


def transform(dir, transformation):
    for constellation_name in os.listdir(dir):
        for img in os.listdir(dir + "/" + constellation_name):
            index1 = img.find('.png')
            index2 = img.find('_')
            if int(img[index2+1:index1]) in range(11):
                image_path = dir + "/" + constellation_name + "/" + img
                image = cv2.imread(image_path)
                for i in range(1, 51):
                    augmented_image = transformation(image=image)['image']
                    image_name = img[:index1] + str(i) + img[index1:]
                    cv2.imwrite((dir + "/" + constellation_name + "/" + image_name), augmented_image)
                augmented_image = transformation(image=image)['image']
                cv2.imwrite((dir + "/" + constellation_name + "/" + img), augmented_image)
                print(f'{img} in {constellation_name} - transformations done')


transformation = A.Compose(
    [
        A.RandomCrop(width=1080, height=1080),
        A.ShiftScaleRotate(shift_limit = 0.05, scale_limit=(0.05, 0.15),
                           rotate_limit= 25, interpolation=cv2.INTER_LINEAR, p=1),
        A.RandomBrightnessContrast(p=0.5),
    ]
)
