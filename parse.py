import xml.etree.ElementTree as Xet
import dbf
import sys
import os

def parse_file(lc_file_name:str, lc_unload_path:str):
    print(lc_file_name, '   ==>  ',lc_unload_path)
    tableUL = dbf.Table(
                        filename=lc_unload_path+'__UL_'+os.path.basename(lc_file_name)+'.dbf',
                        field_specs='name c(250); rname c(250); inn c(12); ogrn c(20); category c(10); type c(15); date c(10)',
                        on_disk=True,
                        codepage='cp1251'
                        )

    tableUL.open(dbf.READ_WRITE)

    tableIP = dbf.Table(
                        filename=lc_unload_path+'__IP_'+os.path.basename(lc_file_name)+'.dbf',
                        field_specs='surname c(80); name c(80); patronymic c(80); inn c(12); ogrnip c(20); category c(10); type c(15); date c(10)',
                        on_disk=True,
                        codepage='cp1251'
                        )
    tableIP.open(dbf.READ_WRITE)

    xmlparse = Xet.parse(lc_file_name)
    root = xmlparse.getroot()

    for i in root.findall('Документ'):
        if len(i.findall('ИПВклМСП'))>0:
            lc_category = 'Микро' if i.attrib['КатСубМСП']=='1' else ('Малые' if i.attrib['КатСубМСП']=='2' else ('Средние' if i.attrib['КатСубМСП']=='3' else ''))
            lc_type = 'Организация' if i.attrib['ВидСубМСП']=='1' else ('ИП' if i.attrib['ВидСубМСП']=='2' else '')
            ld_date = i.attrib['ДатаВклМСП']
            i2 = i.findall('ИПВклМСП')[0]
            lc_inn = i2.attrib['ИННФЛ'] if 'ИННФЛ' in i2.attrib else ''
            lc_ogrnip = i2.attrib['ОГРНИП'] if 'ОГРНИП' in i2.attrib else ''
            lc_surname = ''
            lc_name = ''
            lc_patronymic = ''
            if len(i2.findall('ФИОИП'))>0:
                i3 = i2.findall('ФИОИП')[0]
                lc_surname = i3.attrib['Фамилия'] if 'Фамилия' in i3.attrib else ''
                lc_name = i3.attrib['Имя'] if 'Имя' in i3.attrib else ''
                lc_patronymic = i3.attrib['Отчество'] if 'Отчество' in i3.attrib else ''
            recordIP = {'surname':lc_surname, 'name':lc_name, 'patronymic':lc_patronymic, 'inn':lc_inn, 'ogrnip':lc_ogrnip, 'category':lc_category, 'type':lc_type, 'date':ld_date}
            tableIP.append(recordIP)
        for i4 in i.findall('КатСубМСП'):
            print(i.attrib)
    tableIP.close()

    for i in root.findall('Документ'):
        if len(i.findall('ОргВклМСП'))>0:
            lc_category = 'Микро' if i.attrib['КатСубМСП']=='1' else ('Малые' if i.attrib['КатСубМСП']=='2' else ('Средние' if i.attrib['КатСубМСП']=='3' else ''))
            lc_type = 'Организация' if i.attrib['ВидСубМСП']=='1' else ('ИП' if i.attrib['ВидСубМСП']=='2' else '')
            ld_date = i.attrib['ДатаВклМСП']
            i2 = i.findall('ОргВклМСП')[0]
            lc_full_name = i2.attrib['НаимОрг'] if 'НаимОрг' in i2.attrib else ''
            lc_reduce_name = i2.attrib['НаимОргСокр'] if 'НаимОргСокр' in i2.attrib else ''
            lc_inn = i2.attrib['ИННЮЛ'] if 'ИННЮЛ' in i2.attrib else ''
            lc_ogrn = i2.attrib['ОГРН'] if 'ОГРН' in i2.attrib else ''
            recordUL = {'name':lc_full_name[:250], 'rname':lc_reduce_name[:250], 'inn':lc_inn, 'ogrn':lc_ogrn, 'category':lc_category, 'type':lc_type, 'date':ld_date}
            tableUL.append(recordUL)
    tableUL.close()
    os.remove(lc_file_name)

ln_files_count = len(os.listdir(sys.argv[1]))
ln_counter = 0

for file in os.listdir(sys.argv[1]):
    if file.endswith(".xml"):
        ln_counter=ln_counter+1
        print(ln_counter, ' / ', ln_files_count)
        parse_file(os.path.join(sys.argv[1], file), sys.argv[2])


exit()