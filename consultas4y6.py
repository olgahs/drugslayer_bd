import mysql.connector
from mysql.connector import errorcode
from datetime import date, datetime

config = {
    'user': 'drugslayer',
    'password': 'drugslayer_pwd',
    'host': 'localhost',
    'database': 'disnet_drugslayer',
}

try:
    db = mysql.connector.connect(**config)
    db.autocommit = True
    cursor = db.cursor()
    drug_id = input("Introduzca Drug Id ChEMBL : ")
    #4a
    print("\nPhenotype ID\tPhenotype effect")
    query = str("SELECT phenotype_effect.phenotype_id, phenotype_effect.phenotype_name "
                "FROM phenotype_effect, drug_phenotype_effect "
                "WHERE drug_phenotype_effect.drug_id = %s AND drug_phenotype_effect.phenotype_id = phenotype_effect.phenotype_id "
                "LIMIT 10")
    cursor.execute(query, (drug_id,))

    for row in cursor:
        print(row[0] + "\t" + row[1])

    
    #4b
    print("\nPhenotype ID\t")
    query = str("SELECT phenotype_effect.phenotype_id, phenotype_effect.phenotype_name, drug_phenotype_effect.score "
            "FROM phenotype_effect, drug_phenotype_effect "
            "WHERE drug_phenotype_effect.drug_id = %s "
            "AND drug_phenotype_effect.phenotype_type LIKE 'SIDE EFFECT' "
            "AND drug_phenotype_effect.phenotype_id = phenotype_effect.phenotype_id "
            "ORDER BY drug_phenotype_effect.score DESC LIMIT 10")
    cursor.execute(query, (drug_id,))
    for row in cursor:
        print(row[0], row[1], row[2])

    #6
    query = str("SELECT drug_disease.inferred_score, drug.drug_id, drug.drug_name, disease.disease_id, disease.disease_name "
                "FROM drug_disease, drug, disease "
                "WHERE drug_disease.drug_id = drug.drug_id "
                "AND drug_disease.disease_id = disease.disease_id "
                "AND drug_disease.inferred_score IS NOT null "
                "ORDER BY inferred_score ASC LIMIT 10")
    cursor.execute(query)

    drug_name_id = dict()
    disease_name_id = dict()
    print("\nScore\tDrug name\tDisease name")
    for row in cursor:
        drug_name_id[row[2]] = row[1]
        disease_name_id[row[4]] = row[3]
        print(row[0], row[2], row[4])
      
    while True:
        var_in = input("Introduzca nombre de la relacion a eliminar : ")
        if var_in == "exit":
            exit()  

        dd = var_in.split("-")
        if dd[0] in drug_name_id and dd[1] in disease_name_id:
            drug_id = drug_name_id[dd[0]]
            disease_id = disease_name_id[dd[1]]
            break
        else:
            print("Relacion no valida")

    #print(drug_id, disease_id)
    query = str("SELECT * FROM drug_disease "
                "WHERE drug_id=%s AND disease_id=%s")
    #query = "DELETE FROM drug_disease WHERE drug_id='%s' AND disease_id='%s'" %(drug_id,disease_id)
    cursor.execute(query,(drug_id, disease_id,))

    for row in cursor:
        print (row)

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

finally:
    db.close()
    print( "Connection closed")