import collections
import csv
import re
import json

ID_CIDADE = '2754' # BH
ARQUIVO_LISTA_CEP_ENDERECO = 'cepbr_endereco.csv'
LISTA_BHMAP = 'bhmap_endereco2.json'
LISTA_BHMAP_DESTINO = 'bhmap_endereco.geojson'
LISTA_PALAVRAS = 'bhmap_palavras.txt'

trocas_ruas = {
    'Rua W Cinco': u'Rua Nelson de Paula Pires',
    u'Rua Vovô Faria': u'Rua Pastor Welington Gonçalves',
}

trocas = {
    'Abilio': u'Abílio',
    'Abrao': u'Abrão',
    'Acacias': u'Acácias',
    'Adao': u'Adão',
    'Agua': u'Água',
    'Aguas': u'Águas',
    'Aimores': u'Aimorés',
    'Alemaes': u'Alemães',
    'Alcantara': u'Alcântara',
    'Alipio': u'Alípio',
    'Alvares': u'Álvares',
    'Alvaro': u'Álvaro',
    'Amapa': u'Amapá',
    'Amelia': u'Amélia',
    'America': u'América',
    'Americo': u'Américo',
    'Andre': u'André',
    'Angela': u'Ângela',
    'Angelo': u'Ângelo',
    'Antonia': u'Antônio',
    'Antonio': u'Antônio',
    'Apostolo': u'Apóstolo',
    'Araca': u'Araça',
    'Aragao': u'Aragão',
    'Araujo': u'Araújo',
    'Araxa': u'Araxá',
    'Arcilia': u'Arcília',
    'Argelia': u'Argélia',
    'Artenio': u'Artênio',
    'Assembleia': u'Assembléia',
    'Ascencao': u'Ascenção',
    'Assuncao': u'Assunção',
    'Aurelia': u'Aurélia',
    'Avai': u'Avaí',
    'Badaro': u'Badaró',
    'Balanca': u'Balança',
    'Bambui': u'Bambuí',
    'Barao': u'Barão',
    'Belem': u'Belém',
    'Benario': u'Benário',
    'Betania': u'Betânia',
    'Bicao': u'Bicão',
    'Bicuiba': u'Bicuíba',
    'Bocaiuva': u'Bocaiúva',
    'Bolivia': u'Bolívia',
    'Bonifacio': u'Bonifácio',
    'Br': 'BR',
    'Br116': u'BR-116',
    'Brandao': u'Brandão',
    'Bras': u'Brás',
    'Brasilia': u'Brasília',
    'Bromelia': u'Bromélia',
    'Bromelias': u'Bromélias',
    'Bufalo': u'Búfalo',
    'Bulhoes': u'Bulhões',
    'Caetes': u'Caetés',
    'Cafe': u'Café',
    'Caju': u'Caju',
    'Camara': u'Câmara',
    'Camelias': u'Camélias',
    'Canada': u'Canadá',
    'Candelaria': u'Candelária',
    'Candida': u'Cândida',
    'Candido': u'Cândido',
    'Capitao': u'Capitão',
    'Caraca': u'Caraça',
    'Carandai': u'Carandaí',
    'Carijos': u'Carijós',
    'Cassia': u'Cássia',
    'Ceara': u'Ceará',
    'Cecilia': u'Cecília',
    'Celia': u'Célia',
    'Cemiterio': u'Cemitério',
    'Cesar': u'César',
    'Ceu': u'Céu',
    'Chacara': u'Chácara',
    'Chacaras': u'Chácaras',
    'Chicao': u'Chicão',
    'Chitao': u'Chitão',
    'Cicero': u'Cícero',
    'Cinabrio': u'Cinábrio',
    'Clinica': u'Clínica',
    'Comercio': u'Comércio',
    'Conceicao': u'Conceição',
    'Cond': u'Condomínio',
    'Condominio': u'Condomínio',
    'Conego': u'Cônego',
    'Coracao': u'Coração',
    'Crisostemo': u'Crisóstemo',
    'Cristovao': u'Cristóvão',
    'D\'': u'd\'',
    'D\'Agua': u'd\'Água',
    'Da': 'da',
    'Damiao': u'Damião',
    'Das': 'das',
    'De': 'de',
    'Delio': u'Délio',
    'Diacono': u'Diácono',
    'Dionisio': u'Dionísio',
    'Do': 'do',
    'Dos': 'dos',
    'Dr': u'Doutor',
    'Durao': u'Durão',
    'Duvalia': u'Duvália',
    'E': 'e',
    'Ecologico': u'Ecológico',
    'Eden': u'Éden',
    'Efigenia': u'Efigênia',
    'Emilia': u'Emília',
    'Enio': u'Ênio',
    'Epitacio': u'Epitácio',
    'Ercilia': u'Ercília',
    'Esperanca': u'Esperança',
    'Espirito': u'Espírito',
    'Estevao': u'Estevão',
    'Eugenio': u'Eugênio',
    'Eulario': u'Eulário',
    'Eutalia': u'Eutália',
    'Evangelico': u'Evangélico',
    'Evangelicos': u'Evangélicos',
    'Expedicionario': u'Expedicionário',
    'Expedicionarios': u'Expedicionários',
    'Farmaceutico': u'Farmacêutico',
    'Fabio': u'Fábio',
    'Familia': u'Família',
    'Fatima': u'Fátima',
    'Fe': u'Fé',
    'Feijo': u'Feijó',
    'Florencio': u'Florêncio',
    'Florianopolis': u'Florianópolis',
    'Fulgencio': u'Fulgêncio',
    'Gabaglia': u'Gabáglia',
    'Galvao': u'Galvão',
    'Gardenia': u'Gardênia',
    'Gastao': u'Gastão',
    'Gaucho': u'Gaúcho',
    'Gaviao': u'Gavião',
    'Gemeas': u'Gêmeas',
    'Getulio': u'Getúlio',
    'Glucinio': u'Glucínio',
    'Goias': u'Goiás',
    'Goncalo': u'Gonçalo',
    'Goncalves': u'Gonçalves',
    'Gra': u'Grã',
    'Graca': u'Graça',
    'Gracas': u'Graças',
    'Grao': u'Grão',
    'Gregorio': u'Gregório',
    'Guimaraes': u'Guimarães',
    'Helio': u'Hélio',
    'Helvecio': u'Helvécio',
    'Herminio': u'Hermínio',
    'Hortencia': u'Hortência',
    'Ii': 'II',
    'Iii': 'III',
    'Inacio': u'Inácio',
    'Independencia': u'Independência',
    'India': u'Índia',
    'Indio': u'Índio',
    'Ines': u'Inês',
    'Inocencio': u'Inocêncio',
    'Ipe': u'Ipê',
    'Iraja': u'Irajá',
    'Irma': u'Irmã',
    'Irmaos': u'Irmãos',
    'Isaias': u'Isaías',
    'Itaborai': u'Itaboraí',
    'Itagua': u'Itaguá',
    'Itaite': u'Itaité',
    'Italia': u'Itália',
    'Itau': u'Itaú',
    'Iv': 'IV',
    'Ix': 'IX',
    'Januario': u'Januário',
    'Japao': u'Japão',
    'Jatoba': u'Jatobá',
    'Jau': u'Jaú',
    'Jeronimo': u'Jerônimo',
    'Jerusalem': u'Jerusalém',
    'Jk': 'JK',
    'Joao': u'João',
    'Jose': u'José',
    'Julia': u'Júlia',
    'Julio': u'Júlio',
    'Justica': u'Justiça',
    'Lazaro': u'Lázaro',
    'Leao': u'Leão',
    'Leitao': u'Leitão',
    'Leonisio': u'Leonísio',
    'Libero': u'Líbero',
    'Lidia': u'Lídia',
    'Lidio': u'Lídio',
    'Ligacao': u'Ligação',
    'Lilas': u'Lilás',
    'Lirio': u'Lírio',
    'Lirios': u'Lírios',
    'Livio': u'Lívio',
    'Lobao': u'Lobão',
    'Lotus': u'Lótus',
    'Lourenco': u'Lourenço',
    'Lucia': u'Lúcia',
    'Lucio': u'Lúcio',
    'Maceio': u'Maceió',
    'Magalhaes': u'Magalhães',
    'Magnolia': u'Magnólia',
    'Maranhao': u'Maranhão',
    'Marcio': u'Márcio',
    'Mario': u'Mário',
    'Marques': u'Marquês',
    'Maua': u'Mauá',
    'Melao': u'Melão',
    'Mendonca': u'Mendonça',
    'Mexico': u'México',
    'Militao': u'Militão',
    'Minerio': u'Minério',
    'Missionario': u'Missionário',
    'Moca': u'Moça',
    'Mocambice': u'Moçambique',
    'Monica': u'Mônica',
    'Mourao': u'Mourão',
    'Muller': u'Müller',
    'Nana': u'Naná',
    'Napoleao': u'Napoleão',
    'Narcisio': u'Narcísio',
    'Nazare': u'Nazaré',
    'Negrao': u'Negrão',
    'Nicaragua': u'Nicarágua',
    'Nobrega': u'Nóbrega',
    'Noe': u'Noé',
    'Olegario': u'Olegário',
    'Operario': u'Operário',
    'Orozimbio': u'Orozímbio',
    'Orquidea': u'Orquídea',
    'Osorio': u'Osório',
    'Ou': 'ou',
    'Paixao': u'Paixão',
    'Panama': u'Panamá',
    'Paraiba': u'Paraíba',
    'Paraiso': u'Paraíso',
    'Parana': u'Paraná',
    'Paranavai': u'Paranavaí',
    'Patagonia': u'Patagônia',
    'Patria': u'Pátria',
    'Pecanha': u'Peçanha',
    'Perola': u'Pérola',
    'Perpetua': u'Perpétua',
    'Perpetuo': u'Perpétuo',
    'Pessegos': u'Pêssegos',
    'Petunia': u'Petúnia',
    'Petunias': u'Petúnias',
    'Piaui': u'Piauí',
    'Piraja': u'Pirajá',
    'Pm': 'PM',
    'Policia': u'Polícia',
    'Pora': u'Porã',
    'Praca': u'Praça',
    'Principe': u'Príncipe',
    'Proenca': u'Proença',
    'Resistencia': u'Resistência',
    'Rj': 'RJ',
    'Rodoviario': u'Rodoviário',
    'Rondonia': u'Rondônia',
    'Rosario': u'Rosário',
    'Sacolao': u'Sacolão',
    'Salomao': u'Salomão',
    'Sao': u'São',
    'Sapucai': u'Sapucaí',
    'Sebastiao': u'Sebastião',
    'Sergio': u'Sérgio',
    'Servidao': u'Servidão',
    'Silveria': u'Silvéria',
    'Silvio': u'Sílvio',
    'Simao': u'Simão',
    'Simeoes': u'Simeões',
    'Simiao': u'Simião',
    'Sinha': u'Sinhá',
    'Sitio': u'Sítio',
    'Sp': 'SP',
    'Tamandare': u'Tamandaré',
    'Tapirapeco': u'Tapirapecó',
    'Tarcisio': u'Tarcísio',
    'Teofilo': u'Teófilo',
    'Thome': u'Thomé',
    'Tiao': u'Tião',
    'Tome': u'Tomé',
    'Tres': u'Três',
    'Tristao': u'Tristão',
    'Tupinambas': u'Tupinambás',
    'Uniao': u'União',
    'Vi': 'VI',
    'Vigario': u'Vigário',
    'Vii': 'VII',
    'Viii': 'VIII',
    'Vinicius': 'Vinícius',
    'Vitoria': u'Vitória',
    'Voluntario': u'Voluntário',
    'Voluntarios': u'Voluntários',
    'Walkiria': u'Walkíria',
    'Xangri-la': u'Xangri-lá',
    'Xangri-La': u'Xangri-lá',
    'Xi': 'XI',
    'Xii': 'XII',
    'Xiii': 'XIII',
    'Xiv': 'XIV',
    'Xv': 'XV',
    'Xvi': 'XVI',
    'Xviii': 'XVIII',
    'Xx': 'XX',
    'Xxiii': 'XXIII',
    'Xxviii': 'XXVIII',
    'Ze': u'Zé',
    'Zelia': u'Zélia',
    'Zoologico': u'Zoológico'
}

trocas_tipo = {
    'ACS': 'Acesso',
    'AVE': 'Avenida',
    'ALA': 'Alameda',
    'BEC': 'Beco',
    'EST': 'Estrada',
    'LRG': 'Largo',
    'PCA': u'Praça',
    'RDP': 'Rua de Pedestre',
    'ROD': 'Rodovia',
    'RUA': 'Rua',
    'TRE': 'Trevo',
    'TRV': 'Travessa',
    'TUN': u'Túnel',
    'VDP': 'Via de Pedestre',
    'VDT': 'Viaduto',
    'VIA': 'Via'
}

def normaliza_nome_logra(tipo, nome):
    logradouro = u''

    _tipo = trocas_tipo.get(tipo, tipo) if tipo else ''

    for palavra in nome.title().split():
        logradouro = f'{logradouro} {trocas.get(palavra, palavra)}'.strip()
    
    return f'{_tipo} {logradouro}'


def extrair_logradouros(regiao = -1):
    logradouros = dict()
    tipos = ['Avenida', 'Estrada', 'Praça', 'Rua']

    with open(ARQUIVO_LISTA_CEP_ENDERECO, 'r') as f:
        reader = csv.DictReader(f, delimiter='|')
        for row in reader:
            if row['id_cidade'] == ID_CIDADE:
                nome_logra = row['logradouro']
                tipo_logra = row['tipo_logradouro']
                cep = int(row['cep'])

                nome_logra = re.sub('^((Rua)|(Avenida)|(Praça)|(Alameda))', '', nome_logra).strip()
                nome_logra = re.sub('(\s\d.*)', '', nome_logra).strip()
                
                if tipo_logra:
                    nome_logra = f'{tipo_logra} {nome_logra}'

                    #if nome_logra in trocas_ruas.keys():
                    #    nome_logra = trocas_ruas[nome_logra]

                    if not cep in logradouros.keys():
                        logradouros[cep] = {'nome': nome_logra, 'regional': 0}

    json_data = None

    logradouros['SEM_CEP'] = list()
    logra_sem_cep = logradouros['SEM_CEP']

    _lista_comparar = dict()
    
    # carrega e lê a lista de logradouros
    # do BHMap
    with open(LISTA_BHMAP, 'r') as f:
        json_data = json.load(f)

        json_result = {
            'type': 'FeatureCollection',
            'totalFeatures': 0,
            'features': []
        }

        for feature in json_data['features']:
            properties = feature['properties']

            # obtém as propriedades necessárias para usar no OSM
            logra = properties['NOME_LOGRADOURO']
            tipo_logra = properties['SIGLA_TIPO_LOGRADOURO']
            id_regional = properties['ID_REGIONAL']
            bairro = properties['NOME_BAIRRO_POPULAR']
            numero_imovel = properties['NUMERO_IMOVEL']
            letra_imovel = properties['LETRA_IMOVEL']
            cep = properties['CEP']

            # constrói um objeto para facilitar a filtragem
            obj_logra = {'nome': normaliza_nome_logra(tipo_logra, logra), 'regional': id_regional, 'bairro': bairro, 'numero_imovel': f'{numero_imovel}{letra_imovel if letra_imovel else ""}', 'cep': None}

            # conta quantos digitos para saber se o cep é válido
            if cep:
                import math
                digitos_cep = int(math.log10(cep))+1
                if digitos_cep == 8:
                    cep_str = str(cep)
                    obj_logra['cep'] = f'{cep_str[:5]}-{cep_str[5:]}'

            # detecta se o logradouro da PBH possui CEP e se ele já está na lista
            if cep and cep in logradouros.keys():
                import string
                nome = logradouros[cep]['nome']
                tabela_acentos = str.maketrans('áàâãéèêẽíìîĩóòôõúùûũçÁÀÂÃÉÈÊẼÍÌÎĨÓÒÔÕÚÙÛŨÇ', 'aaaaeeeeiiiioooouuuucAAAAEEEEIIIIOOOOUUUUC', string.punctuation)
                nome_sem_acento = nome.translate(tabela_acentos)

                # compara o nome da lista de CEP com o nome do BHMap
                if nome_sem_acento.lower() != obj_logra['nome'].translate(tabela_acentos).lower():
                    # se o nome é rodovia ou via de ligação, não mudar
                    if nome.startswith('Via de Ligação') or nome.startswith('Rodovia'):
                        obj_logra['nome'] = nome
                        continue

                    # o nome do logradouro será mantido como o nome da PBH somente se ele for totalmente diferente da lista de CEPs

                    if not nome in _lista_comparar.keys():
                        _lista_comparar[nome] = obj_logra['nome']
                else:
                    obj_logra['nome'] = nome
                
                logradouros[cep] = obj_logra
                #print(f'\tCEP {cep} => {nome_logra} => {nome}')

            # adiciona os logradouros sem CEP a uma entrada específica para logradouros sem CEP
            else:
                if not obj_logra in logra_sem_cep:
                    logra_sem_cep.append(obj_logra)
            
            #print(dict(obj_logra))
            properties['addr:street'] = obj_logra['nome']
            properties['addr:postcode'] = obj_logra['cep']
            properties['addr:housenumber'] = obj_logra['numero_imovel']
            properties['addr:suburb'] = obj_logra['bairro']

            if regiao == -1:
                json_result = json_data
            else:
                if regiao == properties['ID_REGIONAL']:
                    json_result['features'].append(feature)
                    json_result['totalFeatures'] = json_result['totalFeatures'] + 1
        
        with open(LISTA_BHMAP_DESTINO, 'w') as out:
            json.dump(json_result, out)

                

    lista_comparar = collections.OrderedDict(sorted(_lista_comparar.items()))
    #for antigo,novo in lista_comparar.items():
        #print(f'{antigo} => {novo}')

    #print(f'# {len(logradouros)}')
    return logradouros

def extrair_salvar_palavras(logradouros):
    palavras = list()

    for logra in logradouros['SEM_CEP']:
        logradouro = logra['nome'][4:]

        for palavra in logradouro.split():
            if not palavra in palavras:
                palavras.append(palavra)
    
    palavras.sort()

    print(f'Foram encontradas {len(palavras)} palavras')

    with open(LISTA_PALAVRAS, 'w') as f:
        for palavra in palavras:
            f.write(f'{palavra}\n')

logradouros = extrair_logradouros(6)
        

#print(logradouros)
#extrair_salvar_palavras(logradouros)