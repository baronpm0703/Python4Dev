import streamlit as st

def fact(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * fact(n - 1)
      
def main():
    st.title("Factorial Calculator")
    number = st.number_input("Enter a number:", min_value=0, max_value=100, value=5)
    if st.button("Calculate"):
        result = fact(number)
        st.write(f"The factorial of {number} is {result}")
        st.balloons()

if __name__ == "__main__":
    main()
