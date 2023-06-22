import numpy as np
import pandas as pd

def spring_weather(temperatures, minTemp, maxTemp): # DONE
	return np.mean(temperatures[(temperatures >= minTemp) & (temperatures < maxTemp)])
	# return temperatures[(temperatures >= minTemp) & (temperatures < maxTemp)]

def random_sale(items, cost, tax, discount, budget): # DONE
	# return np.where(((cost + (1 + tax)) - discount) <= budget, items)
	return items[((cost + tax) - discount) <= budget]

def no_null(data): # DONE
	return np.where(np.isnan(data) == True, np.mean(data[np.isnan(data) != True]), data)

def wordle(player1, player2): # DONE
	return np.min(np.sum(player1, axis=1)) < ((np.min(np.sum(player2, axis=1))))

def csv_parser(filename): # DONE
	return pd.read_csv(open(filename))

def add_new_col_1(df): # DONE
	df["score"] = round((-1/30000) * df.loc[:, "mileage"] + (df.loc[:, "year"]/2022), 3)
	return df

def add_new_col_2(df):
	price_avg = df.loc[:, "price"].mean()

	# return len(df.loc[:, "bidding_time"].str.split(" ")[0][0]) >= 1

	df["relative_price"] = np.where(((df.loc[:, "brand"] == "chevrolet") | (df.loc[:, "brand"] == "dodge") | (df.loc[:, "brand"] == "ford")) & ((df.loc[:, "color"] == "blue") | (df.loc[:, "color"] == "silver")) & (df.loc[:, "bidding_time"].str.contains("days")), (df.loc[:, "price"] - price_avg).astype("int32"), "Not Interested")

	# df["relative_price"][(df[((df.loc[:, "brand"] == "chevrolet") | (df.loc[:, "brand"] == "dodge") | (df.loc[:, "brand"] == "ford")) & ((df.loc[:, "color"] == "blue") | (df.loc[:, "color"] == "silver"))])] = df.loc[:, "price"] - df.loc[:, "price"].mean()
	# df["relative_price"][(df[((df.loc[:, "brand"] != "chevrolet") & (df.loc[:, "brand"] != "dodge") & (df.loc[:, "brand"] != "ford")) | ((df.loc[:, "color"] != "blue") & (df.loc[:, "color"] != "silver"))])] = "Not Interested"

	# df["relative_price"] = int(df.loc[:, "price"] - df.loc[:, "price"].mean()) if (df[((df.loc[:, "brand"] == "chevrolet") | (df.loc[:, "brand"] == "dodge") | (df.loc[:, "brand"] == "ford")) & ((df.loc[:, "color"] == "blue") | (df.loc[:, "color"] == "silver"))]) else "Not Interested"

	return df

def year_data(df): # DONE
	return df.groupby(["brand", "model"]).agg({"year": "count"})

def cannot_a_ford(df): # DONE
	return df[df["brand"] == "ford"].groupby("year").agg({"price": "mean"}).astype("int32")
	
def export_excel(df, filename, sheetname): # DONE
	return df.to_excel(filename, sheet_name=sheetname)


if __name__ == "__main__":
	#Q1
	temperatures = np.array([[70, 85, 58, 61, 68, 80, 77],
						[68, 78, 64, 70, 43, 77, 59]])
	# print(spring_weather(temperatures, 60, 80))

	temperatures = np.array([[72, 81, 55, 56, 86, 53, 75],
						[71, 79, 79, 82, 87, 70, 69],
						[74, 49, 77, 88, 91, 76, 88]])
	# print(spring_weather(temperatures, 70, 85))

	#Q2
	items = np.array(['apple pie', 
		"ben and jerry's mint chocolate chunk", 
		'root beer float', 
		'tiramisu', 
		'cannoli',
		"trader joe's coffee ice cream", 
		'chocolate chip cookie',
		'oatmeal raisin cookie'])
	cost = np.array([15, 6, 6, 12, 7, 7, 6, 6])
	tax = np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
	discount = np.array([2,3,2,1,0,1,2,3])
	# print(random_sale(items, cost, tax, discount, 5))

	#Q3
	data = np.array([92, np.nan, 99, np.nan, np.nan, 80, np.nan, 100, np.nan, 78])
	# print(no_null(data))
	data = np.array([84, 270, 94, np.nan, np.nan, 82, np.nan, 100, np.nan, 18])
	# print(no_null(data))
	
	#Q4
	player1 = np.array([[4,4,4,2,6,6,6],
					[3,2,5,5,5,2,2],
					[1,2,1,5,4,3,3]])
	player2 = np.array([[6,2,3,3,5,4,6],
						[5,3,3,2,1,4,2],
						[1,5,4,3,6,2,4]])
	# print(wordle(player1, player2))

	#Q5
	df = csv_parser("cars.csv")
	# print(df)
	# print(df.shape)


	#Q6
	df = csv_parser("cars.csv")
	df2 = add_new_col_1(df)
	# print(df2)

	#Q7
	df = csv_parser("cars.csv")
	df3 = add_new_col_2(df)
	print(df3)
	print(len(df3[df3["relative_price"] != "Not Interested"]) )

	#Q8
	df = csv_parser("cars.csv")
	df4 = year_data(df)
	# pd.set_option('display.max_rows', df4.shape[0]+1)
	# print(df4)
	# print(df4.shape)

	#Q9
	df = csv_parser("cars.csv")
	# print(cannot_a_ford(df))

	#Q10
	df = csv_parser("cars.csv")
	# export_excel(df, "car_stats.xlsx", "Car Stats")