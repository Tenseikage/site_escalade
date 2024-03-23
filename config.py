from configparser import ConfigParser


def config(filename = "database.ini", section = "postgresql"):
    # creation of a parser
    parser = ConfigParser()
    parser.read(filename)
    database = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            database[param[0]] = param[1]

    else:
        
        raise Exception('Section {0} is not found in the {1}'.format(section,filename))
    
    return database
   

