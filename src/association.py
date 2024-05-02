import pandas as pd
from data_preprocessing import get_cleaned_data
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

def create_dataset(data, num=None):
    dataset = []
    if num is None:
        num = len(data)
    for i in range(0, num):
        dataset.append(list(map(str, data.iloc[i].values.tolist())))
    print("Dataset created")
    return dataset

def start():
    data = get_cleaned_data()

    target_value = 0

    # select only the columns with target = 0
    data = data[data["TARGET"] == target_value]

    # convert numbers to categories
    for col in data.columns:
        data[col] = data[col].map({x: col + "_" + str(x) for x in data[col].unique()})
            
    print(len(data))

    split_by_col = 'NAME_EDUCATION_TYPE'    
    unique_values = data[split_by_col].unique()
    datasets = {}

    for value in unique_values:
        splitted_data = data[data[split_by_col] == value]
        value = value.replace(" ", "_").replace("/", "_").replace("\\", "_")
        print(f"VA {value} has {len(splitted_data)} rows")
        dataset = create_dataset(splitted_data, None)
        te = TransactionEncoder()
        te_ary = te.fit(dataset).transform(dataset)
        df = pd.DataFrame(te_ary, columns=te.columns_)
        frequent_itemsets = apriori(df, min_support=0.6, use_colnames=True)
        print("Freq itemsets created")
        frequent_itemsets.to_csv(f"../data/{value}_frequent_itemsets_{str(target_value)}.csv")
        rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.7)
        print("Rules created")
        rules.to_csv(f"../data/{value}_rules_{(target_value)}.csv")


if __name__ == "__main__":
    start()