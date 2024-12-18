def markdown_to_blocks(markdown):
    lines = markdown.split("\n")
    lines.append("") #add an empty line to the list otherwise we skip the last element
    blocks=[]
    this_line = ""
    for line in lines:
        if line.strip() == "":
            if this_line != "":
                blocks.append(this_line.strip())
                this_line = ""
        else:
            this_line += line+"\n"
    return blocks