from functions.generateRanking import generateSpecificRanking


nome = 'pcp - o Matheus'

years = [2022]
months = [12, 11, 10, 9, 8, 7, 6, 5, 4, 3,2,1]

for year in years:
    for month in months:
        generateSpecificRanking(nome= nome, year=year, month=month)