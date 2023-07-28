import re
from util.StringUtil import remove_acentos, remove_varios_espacos

#regex = '(?:(?:APELACAO\s*CIVEL\s*(?:N.|\:)?\s*|PROCESSO\s*(?:N.)?\:?\s*|NUMERACAO\s*UNICA\s*:\s*)(\\\\\b\d{7}\-?\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}|\\\\\b\d{7}\-?\d{2}\.\d{4}\.\d{3}\.\d{4}|\\\\\b\d{3}\.\d{2}\.\d{6}\-\d|\\\\\b\d{4}\-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}|\\\\\b\d{4}\.\d{2}\.\d{2}\.\d{6}\-\d|\\\\\b\d{3}\-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}|\\\\\b\d{5}\-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4})|\\\\\bN.\s*PROCESSO\s*:\s*(\\\\\b\d{7}\-?\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}|\\\\\b\d{7}\-?\d{2}\.\d{4}\.\d{3}\.\d{4}|\\\\\b\d{3}\.\d{2}\.\d{6}\-\d|\\\\\b\d{4}\-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}|\\\\\b\d{4}\.\d{2}\.\d{2}\.\d{6}\-\d|\\\\\b\d{3}\-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}|\\\\\b\d{5}\-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4})|(\\\\\b\d{7}\-?\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}|\\\\\b\d{7}\-?\d{2}\.\d{4}\.\d{3}\.\d{4}|\\\\\b\d{3}\.\d{2}\.\d{6}\-\d|\\\\\b\d{4}\-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}|\\\\\b\d{4}\.\d{2}\.\d{2}\.\d{6}\-\d|\\\\\b\d{3}\-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}|\\\\\b\d{5}\-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4})(?:(?:\s*\d+\s*)?-\s*\w+|\s*PROT\.:\d{1,2}/\d{1,2}/\d{4}\s*|\s*\d{5,}\s*\w+|[\s*\w+\s*/]+))'
regex = '(?:\s+BANANA\s+(?:PROCESSO\s*N..?.{0,10}\s*-?\s*)(\\b\d{7}\s*[\.\-]\s*?\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}|\\b\d{7}\s*[\.\-]\s*?\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d{3}\s*[\.\-]\s*\d{4}|\\b\d{3}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{6}\s*[\.\-]\s*\d|\\b\d{4}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}|\\b\d{4}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{6}\s*[\.\-]\s*\d|\\b\d{3}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}|\\b\d{5}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}|\\b\d{7}\s*[\.\-]\s*\d\/\d|\\b\d{3}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d{6}\s*[\.\-]\s*\d\\b|\\b\d{3}\s*[\.\-]\s*\d{3}\s*[\.\-]\s*\d\/\d\\b|\\b\d{6,7}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}|\\b\d{3}\s*[\.\-]\s*\d{2}\s*[\.\-]\s*\d{4}\s*[\.\-]\s*\d{6}(\s*[\.\-]\s*\d\/\d{6}\s*[\.\-]\s*\d{3})?|\\b\d{3}\s*[\.\-]\s*\d{2,4}\s*[\.\-]\s*\d{6}\s*[\.\-]?\s*\d?|\d{5,7}\s*[\.\-\/]\s*\d{4}\s*[\.\-\/]\s*\d{3}\s*[\.\-\/]\s*\d{2}\s*[\.\-\/]\s*\d{2}\s*[\.\-\/]?\s*\d|\d{9}20[0-9]{2}5(02|15)\d{4}))'

file = open('/home/e7609043/Downloads/TRT_Judiciario_Caderno_do_TRT_da_2a_Regiao_2019_04_23.txt')

linhas = file.readlines()

linhas = ''.join(linhas).split('\n')
clean_lines = list(map(lambda linha: remove_acentos(linha).upper(), linhas))
clean_lines = list(filter(lambda linha: linha != '', list(map(lambda linha: remove_varios_espacos(re.sub('\s*\n|\t', '', linha)), clean_lines))))
clean_lines = ' BANANA '.join(clean_lines)

splited_lines = re.split(regex, clean_lines)
splited_clean_lines = list(map(lambda linha: re.sub('\sBANANA\s', ' ', linha), list(filter(lambda linha: linha is not None, splited_lines))))[1:]
splited_clean_lines = list(filter(lambda linha: len(linha) > 3, splited_clean_lines))
new_lines = []

for pos, line in enumerate(splited_clean_lines):
  if pos % 2 == 0:
    try:
      new_lines.append(f'{line} {splited_clean_lines[pos+1]}')
    except:
      continue

print(new_lines)


