from PIL import Image

def changecolor(img,path):
    img = img.convert("RGBA")
    data = img.getdata()
    new = []
    for items in data:
        #rgba(37, 150, 190)
        # new.append((items[2],0,items[0],items[3]))
        if items[0] == 48 and items[1] == 48 and items[2] == 48:
            new.append((0,0,0,0))
        # elif items[0] == 0 and items[1] == 98 and items[2] == 123:
        #     new.append((255,0,0,255))
        # elif items[0] == 1 and items[1] == 70 and items[2] == 87:
        #     new.append((255,0,0,255))
        # elif items[0] == 0 and items[1] == 141 and items[2] == 177:
        #     new.append((255, 0, 0, 255))
        # elif items[0] == 1 and items[1] == 57 and items[2] == 71:
        #     new.append((255, 0, 0, 255))
        else:
            new.append(items)
    img.putdata(new)
    img.save(path)

def change_color(img,path):
    img = img.convert("RGBA")
    data = img.getdata()
    new = []
    for items in data:
        new.append((0,0,0,items[3]))
        # if items[0] > 90 and items[1] > 90 and items[2] > 90:
        #     new.append((0, 0, 0, 0))
        # elif items[0] == 0 and items[1] == 98 and items[2] == 123:
        #     new.append((255,0,0,255))
        # elif items[0] == 1 and items[1] == 70 and items[2] == 87:
        #     new.append((255,0,0,255))
        # elif items[0] == 0 and items[1] == 141 and items[2] == 177:
        #     new.append((255, 0, 0, 255))
        # elif items[0] == 1 and items[1] == 57 and items[2] == 71:
        #     new.append((255, 0, 0, 255))
        # else:
        #     new.append(items)
    img.putdata(new)
    img.save(path)

def convertbw(img,path):
    img = img.convert('1')
    img.save(path)

#rgba(37, 150, 190)
for i in range(0,8):
    img = Image.open(f"images/crystal.png")
    img = img.crop((32*i,0,32*(i+1),33))
    changecolor(img,f"images/crystal/{i}.png")
    # change_color(img,f"images/deadman/{i}.png")

    # img.save(f"images/deadman2/{i}.png")
    # convertbw(img,f"images/player/run4/{i}.png")