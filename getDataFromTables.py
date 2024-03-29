import pyodbc

###
#define the empty dictionary
sku_to_group_dict = {}
###

###
#connection details
database = "Finance_Rpt"
connection_string = 'DRIVER={SQL Server};SERVER=sqlrpt1;DATABASE=%s;Trusted_Connection=False;' %(database)
##NO username or password, we don't know why, we suspect it works if you are logged in and by unicorn magic. Or, our server's security is very, very weak
connection = pyodbc.connect(connection_string)
cursor = connection.cursor()
###

###
#if you've not set your transaction so as to not fuck with the database you're gonna have a bad time
def execute_query(sql):
    try:
        assert sql[0:48].lower() == "set transaction isolation level read uncommitted"
        return cursor.execute(sql)
    except (AssertionError):
        print "your sql query didn't set transaction isolation level read uncommitted correctly"
        return None
###

###
#sql command
sql = "SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED DECLARE @Today int; DECLARE @Last_Week int; DECLARE @Last_Week2 int; DECLARE @Last_Week3 int; DECLARE @Last_Week4 int; SET @Today = DATEDIFF(DAY, '2000-01-01', GETDATE()) SET @Last_Week = DATEDIFF(DAY, '2000-01-01', GETDATE() - 7) SET @Last_Week2 = DATEDIFF(DAY, '2000-01-01', GETDATE() - 14) SET @Last_Week3 = DATEDIFF(DAY, '2000-01-01', GETDATE() - 21) SET @Last_Week4 = DATEDIFF(DAY, '2000-01-01', GETDATE() - 28) SELECT OM.Site, SUM((OP.Qty-OP.Cancelled_Qty)*OP.Charge_Price_Per_Unit*Cu.To_GBP_Multiplier) AS Revenue, DATEPART(HOUR,OM.Order_Created) As Hour, Datepart(DAY,OM.Order_Created) as Day, DATEDIFF(DAY,'2000-01-01',OM.Order_Created), D.Day_Of_Week From Finance_Rpt.dbo.Order_Main OM (NOLOCK) INNER JOIN Finance_Rpt.dbo.Order_Product OP (NOLOCK) ON OP.Order_Number = OM.Order_Number INNER JOIN Finance_Rpt.dbo.Currency Cu (NOLOCK) ON Cu.Currency = OM.Currency INNER JOIN Sensu.dbo.Date_D D (NOLOCK) ON DATEPART(Year,D.Full_Date) = DATEPART(Year,OM.Order_Created) AND DATEPART(Month,D.Full_Date) = DATEPART(Month,OM.Order_Created) AND DATEPART(Day,D.Full_Date) = DATEPART(Day,OM.Order_Created) WHERE DATEDIFF(DAY,'2000-01-01', OM.Order_Created) IN (@Today, @Last_Week, @Last_Week2, @Last_Week3, @Last_Week4) GROUP BY OM.Site, Datepart(DAY,OM.Order_Created), DATEPART(HOUR,OM.Order_Created), DATEDIFF(DAY,'2000-01-01',OM.Order_Created), D.Day_Of_Week ORDER BY OM.Site, Datepart(DAY,OM.Order_Created), DATEPART(HOUR,OM.Order_Created)"
###



execute_query(sql)
results = []
for rows in cursor.execute(sql):
    results.append(rows)



connection.close()




