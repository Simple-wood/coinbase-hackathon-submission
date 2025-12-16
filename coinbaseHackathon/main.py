import streamlit as st
import pandas as pd
import plotly.express as px
import utils

OUTCATEGORIES = ["Food", "Travel", "Entertainment", "Subscriptions", "Clothing", "Bills", "Other"]
INCATEGORIES = ["Wages", "Transfers", "Other"]
ESSENTIALS = ["essential expenses", "non essential expenses"]
MONEYFORMAT = "£ {price:.2f}"

st.set_page_config(page_title="Bank statements insights!", layout="wide")
st.title("Statements dashboard")

file = st.file_uploader("Please upload a CSV", type="csv")

if file:
    data = pd.read_csv(file)
    inCategoriesScores = utils.getInCategories(data, INCATEGORIES)
    outCategoriesScores = utils.getOutCategories(data, OUTCATEGORIES)

    essentialsStats = utils.getEssentialsData(data[["Transaction Description", "Money Out"]], ESSENTIALS)

    maxPosO = utils.findMax(outCategoriesScores)
    maxPosI = utils.findMax(inCategoriesScores)

    outdf = pd.DataFrame({'Categories': OUTCATEGORIES,
                         'Money': outCategoriesScores})
    indf = pd.DataFrame({'Categories': INCATEGORIES,
                         'Money': inCategoriesScores})
    
    outFig = px.pie(outdf, values='Money', names='Categories', title="Expenses Breakdown")
    outFig.update_traces(textinfo="label", hovertemplate="<b>%{label}</b><br>" + "Spent: £%{value}<br>")

    inFig = px.pie(indf, values='Money', names='Categories', title="Revenue Breakdown")
    inFig.update_traces(textinfo="label", hovertemplate="<b>%{label}</b><br>" + "£%{value}<br>")

    tab1, tab2, tab3 = st.tabs(["Overview", "Money In", "Money Out"])
    st.divider()
    st.header("Bank statement insights")

    with tab1:
        st.dataframe(data, 
                     column_config={"Balance": st.column_config.NumberColumn(format="£ %.2f"),
                                    "Money In": st.column_config.NumberColumn(format="£ %.2f"),
                                    "Money Out": st.column_config.NumberColumn(format="£ %.2f")})
                
    with tab2:
        st.dataframe(data.loc[data["Money In"] > 0, ["Date", "Transaction Description", "Money In"]],
                     column_config={
                         "Money In": st.column_config.NumberColumn(format="£ %.2f")})
    with tab3:
        st.dataframe(data.loc[data["Money Out"] > 0, ["Date", "Transaction Description", "Money Out"]],
                     column_config={
                         "Money Out": st.column_config.NumberColumn(format="£ %.2f")})

    st.divider()
    
    line_con = st.container(border=True)
    line_con.line_chart(data, x="Date", y="Balance", y_label="Balance (£)", )
    st.divider()

    b1, b2 = st.columns((3,1))
    with b1:
        bar_con = st.container(border=True)
        bar_con.bar_chart(data, x="Date", y=["Money In", "Money Out"], y_label="Amount spent (£)", color=["#29D40A", "#FF0C0C"], stack=False)

    totalMoneyIn = indf["Money"].sum()
    totalMoneyOut = outdf["Money"].sum()
    initialBalance = data["Balance"][0]
    finalBalance = data["Balance"][len(data) - 1]
    percentageChangeB = utils.calculatePercentageChange(finalBalance, initialBalance)

    with b2:
        con1 = st.container(border=True)
        con1.metric("Total Money In", MONEYFORMAT.format(price=totalMoneyIn), "🤑🤑🤑", delta_arrow="off")

        con2 = st.container(border=True)
        con2.metric("Total Money Out", MONEYFORMAT.format(price=totalMoneyOut), "😱😱😱", delta_arrow="off")

        con3 = st.container(border=True)
        con3.metric("Final Balance At The End Of The Month", MONEYFORMAT.format(price=finalBalance), str(percentageChangeB) + "%")

    p1, p2, p3 = st.columns((2, 2, 2))

    with p1:
        pcon1 = st.container(border=True)
        pcon1.plotly_chart(outFig)
    
    with p2:
        pcon2 = st.container(border=True)
        pcon2.plotly_chart(inFig)

    with p3:
        pcon3 = st.container(border=True)
        pcon3.metric("Top spending category - ", OUTCATEGORIES[maxPosO])
        pcon3.metric("You've spent - ", MONEYFORMAT.format(price=outCategoriesScores[maxPosO]), "🤑🤑🤑", delta_arrow="off")

        pcon4 = st.container(border=True)
        pcon4.metric("Your greatest source of revenue is through - ", INCATEGORIES[maxPosI])
        pcon4.metric("You've earned - ", MONEYFORMAT.format(price=inCategoriesScores[maxPosI]), "😱😱😱", delta_arrow="off")

    w1, w2 = st.columns((1, 4))

    with w1:
        wcon1 = st.container(border=True)
        wcon2 = st.container(border=True)
        wcon1.metric("Essential expenses -", MONEYFORMAT.format(price=essentialsStats[1]))
        wcon2.metric("Non essential expenses -", MONEYFORMAT.format(price=essentialsStats[0]))

    with w2:
        wcon3= st.container(border=True)
        wcon3.write("Your bank balance was initially at - " + MONEYFORMAT.format(price=initialBalance) +
                    " . Now at the end of the month, your bank balance is - " + MONEYFORMAT.format(price=finalBalance) + " .")
        
        if initialBalance > finalBalance:
            wcon3.write("Your bank balance is lower than it was initially, you are spending more than you earn!")
            wcon3.write("This reflects a perenctage decrease of " + str(percentageChangeB) + "%")
        
        elif finalBalance > initialBalance:
            wcon3.write("Your bank balance is greater than it was initially, you are spending less than what you earn!")
            wcon3.write("This reflects a percentage increase of " + str(percentageChangeB) + "%")
        
        else:
            wcon3.write("Your bank balance remains the same")

        wcon3.write("Your essential expenses came up to - " + MONEYFORMAT.format(price=essentialsStats[1]))
        wcon3.write("Your non essential expenses came up to - " + MONEYFORMAT.format(price=essentialsStats[0]))
        
else:
    st.write("gimme something")


