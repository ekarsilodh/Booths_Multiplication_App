import streamlit as st
import pandas as pd

#defining page name & icon
st.set_page_config(
    page_title="Booth's Multiplication Calculator",
    page_icon="🧮",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
    }
)

#Font Selection
st.markdown(
    """
    <head>
        <link href='https://fonts.googleapis.com/css?family=Pacifico' rel='stylesheet'>
        <link href='https://fonts.googleapis.com/css?family=Mooli' rel='stylesheet'>
        <link href='https://fonts.googleapis.com/css?family=Orbitron' rel='stylesheet'>
        <link href='https://fonts.googleapis.com/css?family=Roboto' rel='stylesheet'>
        <link href='https://fonts.googleapis.com/css?family=DancingScript' rel='stylesheet'>
        <link href='https://fonts.googleapis.com/css?family=Caveat' rel='stylesheet'>
    </head>
    """,
    unsafe_allow_html=True
)

# Page title
st.markdown(
    """
    <h1 style='text-align: center; font-family: Pacifico, sans-serif'>Booth's Multiplication Calculator</h1>
    """,
    unsafe_allow_html=True
)


def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    dt = pd.DataFrame(df)
    return dt.to_csv().encode('utf-8')


def dectobin(num):
    a = bin(num).replace("0b","")
    if len(str(a)) < 4:
        a = str(a).zfill(4)
        return a
    else:
        return a 

def tcomplement(neg):
    a = bin(neg).replace("0b","")
    num = str(a).zfill(4) if len(str(a)) < 4 else str(a).zfill(1 + len(str(a)))
        #print(num)
    
    lst = []
    for i in num:
        if i == '1':
            lst.append(str(0))
        elif i == '0':
            lst.append(str(1))
    b = ''.join(lst)
    complement = bin(int(b, 2) + int("1", 2)).replace("0b","")
    return complement

def tcomp(x):
    lst = [str(1) if i == '0' else str(0) for i in x]
    b = ''.join(lst)
    complement = bin(int(b, 2) + int("1", 2)).replace("0b","")
    return str(complement).zfill(len(b)) if len(str(complement)) < len(b) else str(complement)

def ficbit(x):
    q = str(x) + '0'
    return q 

def ars(x, y):
    l1 = [i for i in x]
    l2 = [i for i in y]
    l1 += l2 
    #print(l1)
    b = ''.join(l1)
    #print(b)
    num = int(b, 2)
    num = num >> 1
    c = bin(num).replace("0b","")
    #print(c)
    if l1[0] == '0':
        c = str(c).zfill(len(b))
        return c 
    elif l1[0] == '1':
        z = '1' * (len(b)-len(str(c)))
        c = z + c
        return c

def ad(x, y):
    l = bin(int(x, 2) + int(y, 2)).replace("0b", "")
    return l 

def sb(x, y):
    z = tcomp(y)
    #print("z=", z)
    l = bin(int(x, 2) + int(z, 2)).replace("0b","")
    if len(str(l)) < len(str(x)):
        l = str(l).zfill((len(str(x))))
        #print(l)
        return l 
    elif len(str(l)) > len(str(x)):
        l = l[-a_bit:]
        return l
    else:
        return l 

#print("\nBooth's Multiplication Calculator\n")

no1 = st.text_input("Enter the 1st no.")
no2 = st.text_input("Enter the 2nd no.")

if st.button("Calculate"):
    if no1 and no2:
        a = int(no1)
        b = int(no2)
        M = dectobin(a) if a > 0 else tcomplement(a)
        Q = dectobin(b) if b > 0 else tcomplement(b)

        #initialize the accumulator.
        A = '0' * len(str(M))
        size = len(str(Q))
        #print(size)

        #bits in A & Q
        a_bit = len(str(A))
        q_bit = len(str(Q))
        #print(a_bit)
        #print(q_bit)

        #adding the fictious bit to Q.
        Qf = ficbit(Q)
        #print(Qf)
        qf_bit = len(str(Qf))


        data = [["Operation", "M", "A", "Q", "Size"]]
        data.append(['Initial', M, A, Qf, size])
        print(data)


        #iteration for steps.
        while(size!=0):
            size -= 1

            if (Qf[-2:] == '00'):
                z = ars(A, Qf)
                A = z[:a_bit]
                Qf = z[-qf_bit:]

                calc_data = ['Q[0]=0 & Q[-1]=0 ARS(AQ)', str(M), str(A), str(Qf), size]
                data.append(calc_data)

            elif (Qf[-2:] == '11'):
                z = ars(A, Qf)
                A = z[:a_bit]
                Qf = z[-qf_bit:]

                calc_data = ['Q[0]=1 & Q[-1]=1 ARS(AQ)', str(M), str(A), str(Qf), size]
                data.append(calc_data)

            elif (Qf[-2:] == '01'):
                A = ad(A, M)

                calc_data = ['Q[0]=0 & Q[-1]=1 A=A+M', str(M), str(A), str(Qf), '-']
                data.append(calc_data)

                z = ars(A, Qf)
                A = z[:a_bit]
                Qf = z[-qf_bit:]

                calc_data = ['ARS(AQ)', str(M), str(A), str(Qf), size]
                data.append(calc_data)

            elif (Qf[-2:] == '10'):
                A = sb(A, M)
                #print(A)

                calc_data = ['Q[0]=1 & Q[-1]=0 A=A-M', str(M), str(A), str(Qf), '-']
                data.append(calc_data)

                z = ars(A, Qf)
                #print("z=", z)
                A = z[:a_bit]
                #print('A=', A)
                Qf = z[-qf_bit:]
                #print('Qf =', Qf)

                calc_data = ['ARS(AQ)', str(M), str(A), str(Qf), size]
                data.append(calc_data)

        #result calculation
        l1 = [i for i in A]
        l2 = [i for i in Qf]
        l1 += l2
        r_bit = a_bit + q_bit
        res_join = ''.join(l1)
        result = res_join[:r_bit]


        #print("\n")

        st.write(f"M = {a} = {M}")
        st.write(f"Q = {b} = {Q}")
        #print(data)
        #print("\n")
        # Convert the string data into a pandas DataFrame
        #data = StringIO(tb(data, headers=["Operation", "M", "A", "Q", "Size"]))
        #df = pd.read_csv(data, sep='\s+')

        st.table(data)
        st.success(f"The result is: {result}")


        csv = convert_df(data)

        st.download_button("Download CSV", data=csv, file_name='Booths.csv')
    else:
        st.error("Enter the nos!!!")

#Font Selection
st.markdown(
    """
    <head>
        <link href='https://fonts.googleapis.com/css?family=Pacifico' rel='stylesheet'>
        <link href='https://fonts.googleapis.com/css?family=Mooli' rel='stylesheet'>
        <link href='https://fonts.googleapis.com/css?family=Orbitron' rel='stylesheet'>
        <link href='https://fonts.googleapis.com/css?family=Roboto' rel='stylesheet'>
        <link href='https://fonts.googleapis.com/css?family=DancingScript' rel='stylesheet'>
        <link href='https://fonts.googleapis.com/css?family=Caveat' rel='stylesheet'>
    </head>
    """,
    unsafe_allow_html=True
)

gmail_icon = "E:\Python Projects\Streamlit\mail_icon.png"
gmail_link = "mailto:ekarsilodh@gmail.com"

# Page title
st.markdown(
    """
    <h4 style='text-align: right; font-family: 'Roboto', cursive'; font-size: 25px>Designed & Maintained by</h4>
    <h3 style='text-align: right; font-family: 'Caveat', cursive'; font-size: 25px>Ekarsi Lodh</h3>
    <h4 style='text-align: centered; font-family: 'Dancing Script', sans-serif'; font-size: 20px>Let's Keep in Touch!</h4>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <li><a href="mailto:ekarsilodh@gmail.com">Gmail</a></li>
    <li><a href="https://www.linkedin.com/in/ekarsi-lodh" target="_blank">LinkedIn</a></li>
    """,
    unsafe_allow_html=True
)


