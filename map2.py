# import webbrowser
#
#
# def maps(des1, des2):
#     url = "https://www.google.com/maps/dir/" + des1 + "/" + des2
#     webbrowser.open(url)
#     return
#
#
# maps("nampally", "mehdipatnam")

a = 'jarvis tell me the best route from nampally to mehdipatnam'
# a = a.strip()

# Split the string by 'from' and get the second element
p = a.split('from')[-1]

# Split the second element by 'to' and get both locations as a list
p = p.split('to')

# Join the locations with a space and print them
print(p)