from pygoogle_image import image as pi

file = open("keywords.txt", "r", encoding="utf-8")

for line in file:
  pi.download(line, limit=10)
