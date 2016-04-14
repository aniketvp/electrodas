import glob
import re

PATH = 'H:/SPRING 16/Natural Language Processing/Project/Data/*/*/*.txt'
VERSE_SEPARATOR = "^^^^^^^^^^#"
HALF_VERSE_SEPARATOR = "^^^^^^^%"
LINE_SEPARATOR = "^^^^^$"
FOOTER_TEXT = "This text is part of the TITUS"

def main():
    global PATH, VERSE_SEPARATOR, HALF_VERSE_SEPARATOR, LINE_SEPARATOR, FOOTER_TEXT
    
    with open("regularized_data.txt", 'w', encoding="utf8") as outputfile:
        
        for file in glob.glob(PATH):
            
            with open(file, 'r', encoding="utf8") as inputfile:
                
                chapter = inputfile.read()
                chapter_without_footer = chapter.split(FOOTER_TEXT)[0]
                verses = chapter_without_footer.split("Verse:")
                verses = verses[1:]
                
                for verse in verses:
                    
                    verse = re.sub('/[\d]*/', '//', verse)
                    outputfile.write(VERSE_SEPARATOR)
                    halfverses = re.split('Halfverse: (?:[a-z])', verse)
                    halfverses = halfverses[1:]
                    
                    for halfverse in halfverses:
                        
                        halfverse.strip()
                        outputfile.write(HALF_VERSE_SEPARATOR)
                        lines = halfverse.split("\n");
                        
                        for line in lines:
                            
                            if not line == '':
                                outputfile.write(LINE_SEPARATOR)
                                line = re.sub('/[^\/]*', '/', line)
                                outputfile.write(line.strip())
    
if __name__=="__main__":
    main()