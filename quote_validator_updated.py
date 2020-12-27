file = open('C:\\Users\\Goldy\\Desktop\\data_csv.csv', 'r')

separator = ','

"""reading the contents, each line as string in a list"""
contents = file.readlines()
# print(contents)
"""getting the header"""
header = contents[1]
"""counting  " in the header"""
quote_count_header = header.count('"')
print(quote_count_header)
bad_lines = []
primary_key_name = 'id'
col_names = header.replace('\n', '').split(separator)
primary_key_position = col_names.index('"'+primary_key_name+'"')
for line in contents[2:-1]:
    """comparing " in line with header"""
    if line.count('"') != quote_count_header:
        bad_record = line.split(separator)[primary_key_position]
        for pos, word in enumerate(line.replace('\n', '').split(separator)):
            if word.count('"') != 2:
                bad_lines.append(bad_record+','+col_names[pos]+','+word+'\n')


print("Number of bad records", len(bad_lines))
"""opening a file to write"""
file_write = open('bad_lines.csv', 'w')
"""writing the header"""
file_write.write('"primary_key","col_name","value"\n')
"""write the bad lines"""
file_write.writelines(bad_lines)

"""Closing the files"""
file_write.close()
file.close()




