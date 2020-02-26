
def writetemp(cancer,healthy,lcd):
    lcd.clear()
    lcd.write_string('cancer temp :'+str(cancer)+"\r\n" )
    lcd.write_string('healthy temp :'+str(healthy))
