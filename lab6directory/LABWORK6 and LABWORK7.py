import numpy as np
import pandas as pd

####1
catalog_products=pd.read_excel(r"C:\Users\Пользователь\OneDrive\Документы\catalog_products.xlsx")

# print(f"Строк и столбцов:{catalog_products.shape}\n\n")
#
# print(f"Типы данных каждой колонки:\n{catalog_products.dtypes}\n\n")
#
# print(f"Пропущенные значения:\n")
#
# print("Нет пропущенных значений" if catalog_products.isnull().sum().sum()==0
#       else catalog_products.isnull().sum()[catalog_products.isnull().sum()>0])



####2
numeric=catalog_products.apply(pd.to_numeric,errors="coerce")

numeric_columns=numeric.columns[numeric.notnull().any()]

catalog_products[numeric_columns]=catalog_products[numeric_columns].apply(pd.to_numeric,errors="coerce")

catalog_products[numeric_columns]=catalog_products[numeric_columns].fillna(
    catalog_products[numeric_columns].mean()
)

test=catalog_products[numeric_columns].isnull().sum().sum()

# if test==0:
#     print("Пропусков нет")
# else:
#     print(test)


####3
catalog_products["total_value"]=catalog_products["col_2"]*catalog_products["col_3"]

catalog_products["double_stock"]=catalog_products["col_5"]*2

catalog_products["log_price"]=np.log(catalog_products["col_2"])

#print(catalog_products[["col_1","col_2","total_value","double_stock","log_price"]])


####4
electronics_expensive=catalog_products[(catalog_products["col_2"]>500) &
                                       (catalog_products["col_7"]=="Electronics")]

#print(f"Электронные товары с ценами дороже 500:\n"
      #f"{electronics_expensive[["col_2","col_7"]].head(5)}")


####5
categories_grouped=catalog_products.groupby("col_7").agg(
    mean_price=("col_2","mean"),
    max_price=("col_2","max"),
    total_quantity=("col_3","sum")
).reset_index()

categories_grouped=categories_grouped.rename(columns={"col_7":"categories"})

#print(f"Группировка товаров по категории:\n{categories_grouped.head(5)}")


####6
cols=["col_2","col_3","col_5","col_6","col_8","col_9","col_11","col_12","col_14","col_15"]

# stat=pd.DataFrame({
#     "column":cols,
#     "mean":catalog_products[cols].mean().values,
#     "median":catalog_products[cols].median().values,
#     "std":catalog_products[cols].std().values
# })

#print(stat)

####7
high=catalog_products["col_2"].mean()+(catalog_products["col_2"].std()*3)

anomalies=catalog_products["col_2"][catalog_products["col_2"]>high]
#
# if anomalies.empty:
#     print("Никаких аномальных товаров")
# else:
#     print(anomalies)


####8
corr_matrix=catalog_products[cols].corr()

#print(corr_matrix)



####9
import matplotlib.pyplot as plt

# plt.figure(figsize=(10,6))
# plt.hist(catalog_products["col_2"],bins=50,color="green",edgecolor="black")
#
# plt.title("Распределение цены товаров")
# plt.xlabel("Цена")
# plt.ylabel("Количество товаров")
# plt.grid(True)
#
# plt.show()

####10
import seaborn as sns

# plt.figure(figsize=(10,6))
#
# sns.regplot(data=catalog_products,x="col_2",y="col_3",
#             scatter_kws={"alpha":0.3},
#             line_kws={"color":"red"})
#
# plt.title("Взаимосвязь цены и количества товара")
# plt.xlabel("Цена")
# plt.ylabel("Количество на складе")
# plt.grid(True)
#
# plt.show()

####11
# plt.figure(figsize=(10,6))
# sns.boxplot(data=catalog_products,x="col_7",y="col_2")
#
# plt.xlabel("Категория")
# plt.ylabel("Цена")
#
# plt.grid(True)
#
# plt.show()


####12
# cols=["col_2","col_3","col_5","col_6"]
#
# sns.pairplot(data=catalog_products[["col_7"]+cols],hue="col_7")
#
# plt.show()

####13
#чекай 6 и 8 задачи

# sns.heatmap(corr_matrix,annot=True,fmt=".2f",cmap="coolwarm",vmin=-1,vmax=1)
#
# plt.title("Коррелляция числовых колонок")
# plt.show()


####14
#catalog_products.to_excel("catalog_analysis.xlsx",index=False)

####15
category_summary=catalog_products.groupby("col_7").agg(
    count=("col_2","count"),
    mean_price=("col_2","mean"),
    total_quantity=("col_3","sum"),
    mean_log_price=("log_price","mean")
).reset_index()

category_summary=category_summary.rename(columns={"col_7":"category"})

#category_summary.to_excel("category_summary.xlsx",index=False)


####16
most_expensive=catalog_products.loc[
    catalog_products.groupby("col_7")["col_2"].idxmax()
]

#print(most_expensive[["col_2","col_7"]])


####17
#top_products=catalog_products.sort_values(by="total_value",ascending=False)

#print(top_products[["col_1","col_2","col_3","total_value"]].head(10))

####19
# total_values=catalog_products.groupby("col_7").agg(
#     total_stock_value=("total_value","sum")
# ).reset_index()

# plt.bar(total_values["col_7"],total_values["total_stock_value"],color="skyblue")
#
# plt.title("Категорий с суммарной стоимостью")
# plt.xlabel("Категория")
# plt.ylabel("(col_2 * col_3)")

#plt.show()

# top_total=total_values.loc[total_values["total_stock_value"].idxmax()]

#print(f"Категория товара с наибольшой суммарной стоимостью:\n{top_total}")



####20
# categories_mean=catalog_products.groupby("col_7").agg(
#     mean_price=("col_2","mean"),
#     mean_quantity=("col_3","mean")
# ).reset_index()

# sns.scatterplot(data=categories_mean,x="mean_price",y="mean_quantity",hue="col_7")
#
# plt.title("Средние цены и запасы по категориям товаров")
# plt.xlabel("Средняя цена")
# plt.ylabel("Средний запас")
#
# plt.show()

####21
categories_std=catalog_products.groupby("col_7").agg(
    std_price=("col_2","std")
).reset_index()

categories_std=categories_std.rename(columns={"col_7":"categories"})

# sns.barplot(data=categories_std,x="std_price",y="categories")
#
# plt.show()

####23
# categories_quantity=catalog_products.groupby("col_7").agg(
#     count=("col_3","count")
# ).reset_index()


# plt.bar(categories_quantity["col_7"],categories_quantity["count"],color="skyblue")
#
# plt.show()


####24
# most_popular=catalog_products.sort_values(by="col_3",ascending=False).head(10)
#
# most_popular["product"]="Товар #"+most_popular.index.astype(str)

# sns.barplot(data=most_popular,x="col_3",y="product")
#
# plt.title("Топ 10 товаров по популярности")
#
# plt.show()

####36-41
#те же самые задачи что и 20-25 задачи


####42
# sns.regplot(data=catalog_products,x="col_2",y="col_5",
#             scatter_kws={"alpha":0.3},
#             line_kws={"color":"yellow"})

# plt.title("Взаимосвязь цены и рейтинга товаров")
# plt.xlabel("Цена")
# plt.ylabel("Рейтинг")
#
# plt.show()

####43
#то же самое что и 12 задача


####44
#то же самое что и 7 задача

####45
top10_value=catalog_products.sort_values(by="total_value",ascending=False).head(10)
top10_stock=catalog_products.sort_values(by="col_3",ascending=False).head(10)

with pd.ExcelWriter("catalog_final_report.xlsx",engine="openpyxl")as writer:
    catalog_products.to_excel(writer,sheet_name="Обработанные данные",index=False)
    category_summary.to_excel(writer,sheet_name="Отчет по категориям",index=False)
    top10_price.to_excel(writer,sheet_name="Топ-10 по стоимости",index=False)
    top10_stock.to_excel(writer,sheet_name="Топ-10 по количеству",index=False)


