# Utilidades relacionadas à importação de dados do BHMap

## extrair-logra-cep

Script em Python que compara os logradouros do BHMap com uma lista de CEPs encontrada na internet, datada de 2017. A preferência é manter os dados do BHMap, entretanto se um endereço for exatamente igual ao da lista de CEPs, a preferência é da lista de CEPs, já que o endereço já está com o nome correto.

Requer `cepbr_endereco.csv` e a camada de endereços do BHMap, em GeoJSON.