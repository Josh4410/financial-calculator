import tkinter as tk
from tkinter import ttk, scrolledtext
import math
from decimal import Decimal, getcontext
import sv_ttk
# Set decimal precision
getcontext().prec = 10

class FinancialCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Financial Calculator")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Verdana", 10))
        self.style.configure("TButton", font=("Verdana", 10))
        self.style.configure("TEntry", font=("Verdana", 10))
        self.style.configure("Header.TLabel", font=("Verdana", 12, "bold"))
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left frame for inputs
        input_frame = ttk.LabelFrame(main_frame, text="Financial Variables", padding="10")
        input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Right frame for results
        result_frame = ttk.LabelFrame(main_frame, text="Calculation Results", padding="10")
        result_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Scrolled text widget for results
        self.result_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, width=40, height=30)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        self.result_text.config(font=("Courier", 10))
        
        # Create input fields with labels
        self.entries = {}
        
        # List of input fields
        fields = [
            ("PV", "Present Value (PV):"),
            ("FV", "Future Value (FV):"),
            ("r", "Interest Rate (r) [decimal]:"),
            ("n", "Number of Years (n):"),
            ("m", "Compounding Periods/Year (m):"),
            ("PMT", "Regular Payment (PMT):"),
            ("C", "Constant Payment (C):"),
            ("g", "Growth Rate (g) [decimal]:"),
            ("F", "Face Value (F) for Bond:"),
            ("net_income", "Net Income:"),
            ("V", "Value (V):"),
            ("reserve_ratio", "Reserve Ratio:"),
            ("BV", "Beginning Value (BV):"),
            ("EV", "Ending Value (EV):"),
            ("c", "Cash Flows (c):"),
            ("returns", "Returns (comma/space separated):"),
            ("rf_rate", "Risk-Free Rate (rf) [decimal]:"),
            ("beta", "Beta (β):"),
            ("market_premium", "Market Risk Premium [decimal]:")
        ]
        
        # Create a frame for each input field
        for i, (field_name, field_label) in enumerate(fields):
            frame = ttk.Frame(input_frame)
            frame.pack(fill=tk.X, pady=5)
            
            label = ttk.Label(frame, text=field_label, width=25)
            label.pack(side=tk.LEFT)
            
            entry = ttk.Entry(frame)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            entry.insert(0, "0")
            
            self.entries[field_name] = entry
        
        # Buttons frame
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Calculate button
        calculate_button = ttk.Button(
            button_frame, 
            text="Calculate", 
            command=self.calculate
        )
        calculate_button.pack(side=tk.LEFT, padx=5)
        
        # Clear button
        clear_button = ttk.Button(
            button_frame, 
            text="Clear All", 
            command=self.clear_all
        )
        clear_button.pack(side=tk.LEFT, padx=5)
        
        # Help button
        help_button = ttk.Button(
            button_frame, 
            text="Show Available Calculations", 
            command=self.show_help
        )
        help_button.pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status = ttk.Label(main_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)
        
    def get_float_value(self, field_name):
        """Get float value from entry or 0 if invalid"""
        try:
            return float(self.entries[field_name].get())
        except ValueError:
            return 0
        
    def calculate(self):
        """Perform financial calculations based on input values"""
        # Clear previous results
        self.result_text.delete(1.0, tk.END)
        
        #Dictionary to track which variables have been provided
        provided = {}
        
        # Get values from entry fields
        PV = self.get_float_value("PV")
        provided['PV'] = PV != 0
        
        FV = self.get_float_value("FV")
        provided['FV'] = FV != 0
        
        r = self.get_float_value("r")
        provided['r'] = r != 0
        
        n = self.get_float_value("n")
        provided['n'] = n != 0
        
        m = self.get_float_value("m")
        provided['m'] = m != 0
        
        PMT = self.get_float_value("PMT")
        provided['PMT'] = PMT != 0
        
        C = self.get_float_value("C")
        provided['C'] = C != 0
        
        g = self.get_float_value("g")
        provided['g'] = g != 0
        
        F = self.get_float_value("F")
        provided['F'] = F != 0
        
        net_income = self.get_float_value("net_income")
        provided['net_income'] = net_income != 0
        
        V = self.get_float_value("V")
        provided['V'] = V != 0
        
        reserve_ratio = self.get_float_value("reserve_ratio")
        provided['reserve_ratio'] = reserve_ratio != 0
        
        # Get HPY specific values
        BV = self.get_float_value("BV")
        provided['BV'] = BV != 0
        
        EV = self.get_float_value("EV")
        provided['EV'] = EV != 0
        
        c = self.get_float_value("c")
        provided['c'] = c != 0
        
        # Get CAPM specific values
        rf_rate = self.get_float_value("rf_rate")
        provided['rf_rate'] = rf_rate != 0
        
        beta = self.get_float_value("beta")
        provided['beta'] = beta != 0
        
        market_premium = self.get_float_value("market_premium")
        provided['market_premium'] = market_premium != 0
        
        # Get returns input for standard deviation
        returns_str = self.entries["returns"].get().strip()
        returns = []
        if returns_str:
            try:
                # Parse comma-separated or space-separated values
                if ',' in returns_str:
                    returns = [float(x.strip()) for x in returns_str.split(',') if x.strip()]
                else:
                    returns = [float(x) for x in returns_str.split() if x.strip()]
                
                # Convert percentage inputs to decimal if they appear to be percentages
                if any(abs(r) > 1 for r in returns):
                    returns = [r/100 for r in returns]
                
                provided['returns'] = len(returns) > 1
            except ValueError:
                self.result_text.insert(tk.END, "Error: Invalid format in returns data. Use comma or space separated numbers.\n\n")
                provided['returns'] = False
        
        # Begin calculations
        self.result_text.insert(tk.END, "FINANCIAL CALCULATIONS RESULTS\n")
        self.result_text.insert(tk.END, "==============================\n\n")
        
        calculations_performed = 0
        
        # CAPM calculation
        if provided['rf_rate'] and provided['beta'] and provided['market_premium']:
            try:
                # Expected Return = Risk-Free Rate + β × Market Risk Premium
                expected_return = rf_rate + (beta * market_premium)
                self.result_text.insert(tk.END, f"CAPM Expected Return Calculation\n")
                self.result_text.insert(tk.END, f"-----------------------------\n")
                self.result_text.insert(tk.END, f"Risk-Free Rate (rf) = {rf_rate:.4f}\n")
                self.result_text.insert(tk.END, f"Beta (β) = {beta:.4f}\n")
                self.result_text.insert(tk.END, f"Market Risk Premium = {market_premium:.4f}\n")
                self.result_text.insert(tk.END, f"Expected Return = {rf_rate:.4f} + ({beta:.4f} × {market_premium:.4f})\n")
                self.result_text.insert(tk.END, f"Expected Return = {expected_return:.4f}\n")
                self.result_text.insert(tk.END, f"Expected Return (%) = {expected_return*100:.2f}%\n\n")
                calculations_performed += 1
            except ValueError as e:
                self.result_text.insert(tk.END, f"Error in CAPM calculation: {str(e)}\n\n")
        
        # Standard Deviation calculation
        if provided.get('returns', False):
            try:
                # Calculate mean return
                mean_return = sum(returns) / len(returns)
                
                # Calculate squared deviations
                squared_diffs = [(r - mean_return)**2 for r in returns]
                sum_squared_diffs = sum(squared_diffs)
                
                # Calculate sample variance (divide by n-1)
                if len(returns) > 1:  # Must have at least 2 data points for sample std dev
                    sample_variance = sum_squared_diffs / (len(returns) - 1)
                    # Calculate standard deviation
                    sample_std_dev = math.sqrt(sample_variance)
                    
                    # Display results
                    self.result_text.insert(tk.END, f"Returns Analysis\n")
                    self.result_text.insert(tk.END, f"----------------\n")
                    self.result_text.insert(tk.END, f"Returns: {[f'{r:.4f}' for r in returns]}\n")
                    self.result_text.insert(tk.END, f"Mean Return = {mean_return:.4f}\n")
                    
                    # Show calculation details
                    self.result_text.insert(tk.END, f"Squared Deviations:\n")
                    for i, r in enumerate(returns):
                        dev = r - mean_return
                        sq_dev = dev**2
                        self.result_text.insert(tk.END, f"  Return {i+1}: {r:.4f} → Dev: {dev:.4f} → Sq Dev: {sq_dev:.6f}\n")
                    
                    self.result_text.insert(tk.END, f"Sum of Squared Deviations = {sum_squared_diffs:.6f}\n")
                    self.result_text.insert(tk.END, f"Sample Variance (σ²) = {sample_variance:.6f}\n")
                    self.result_text.insert(tk.END, f"Sample Standard Deviation (σ) = {sample_std_dev:.6f}\n")
                    self.result_text.insert(tk.END, f"Sample Standard Deviation (%) = {sample_std_dev*100:.2f}%\n\n")
                    calculations_performed += 1
                else:
                    self.result_text.insert(tk.END, "Warning: Need at least 2 return values to calculate standard deviation\n\n")
            except ValueError as e:
                self.result_text.insert(tk.END, f"Error in standard deviation calculation: {str(e)}\n\n")
        
        # Holding Period Yield (HPY)
        if provided['BV'] and provided['EV'] and provided['n']:
            try:
                # Annual HPY = ((EV+c)/BV)^(1/n) - 1
                # Make sure to include cash flows if provided
                numerator = EV
                if provided['c']:
                    numerator += c
                
                hpy = ((numerator / BV) ** (1/n)) - 1
                self.result_text.insert(tk.END, f"Annual Holding Period Yield (HPY) = {hpy:.4f}\n")
                self.result_text.insert(tk.END, f"Annual Holding Period Yield (HPY) % = {hpy*100:.2f}%\n\n")
                calculations_performed += 1
            except ZeroDivisionError:
                self.result_text.insert(tk.END, "Error: Beginning Value (BV) cannot be zero for HPY calculation\n\n")
            except ValueError:
                self.result_text.insert(tk.END, "Error: Cannot compute HPY with negative values resulting in complex numbers\n\n")
        
        # Credit multiplier
        if provided['reserve_ratio']:
            try:
                credit_multiplier = 1 / reserve_ratio
                self.result_text.insert(tk.END, f"Credit Multiplier = {credit_multiplier:.4f}\n\n")
                calculations_performed += 1
            except ZeroDivisionError:
                self.result_text.insert(tk.END, "Error: Reserve ratio cannot be zero for Credit Multiplier\n\n")
        
        # Simple interest
        if provided['PV'] and provided['r'] and provided['n']:
            I = PV * r * n
            self.result_text.insert(tk.END, f"Simple Interest (I) = {I:.4f}\n")
            
            # FV = PV(1+r*n)
            FV_simple = PV * (1 + r * n)
            self.result_text.insert(tk.END, f"Future Value (Simple Interest) = {FV_simple:.4f}\n\n")
            calculations_performed += 1
        
        if provided['FV'] and provided['r'] and provided['n']:
            # PV = FV / (1+r*n)
            try:
                PV_simple = FV / (1 + r * n)
                self.result_text.insert(tk.END, f"Present Value (Simple Interest) = {PV_simple:.4f}\n\n")
                calculations_performed += 1
            except ZeroDivisionError:
                self.result_text.insert(tk.END, "Error: Division by zero in Present Value calculation\n\n")
        
        # FV/PV of Single Payment
        if provided['PV'] and provided['r'] and provided['n']:
            # FV = PV(1+r)^n
            FV_compound = PV * ((1 + r) ** n)
            self.result_text.insert(tk.END, f"Future Value (Single Payment) = {FV_compound:.4f}\n\n")
            calculations_performed += 1
        # Present Value
        if provided['FV'] and provided['r'] and provided['n']:
            # PV = FV / (1+r)^n
            try:
                PV_compound = FV / ((1 + r) ** n)
                self.result_text.insert(tk.END, f"Present Value (Single Payment) = {PV_compound:.4f}\n\n")
                calculations_performed += 1
            except ZeroDivisionError:
                self.result_text.insert(tk.END, "Error: Division by zero in Present Value calculation\n\n")
        
        # Multiple compounding periods
        if provided['PV'] and provided['r'] and provided['n'] and provided['m']:
            # FV = PV*(1+(r/m))^(m*n)
            try:
                FV_multi = PV * ((1 + (r / m)) ** (m * n))
                self.result_text.insert(tk.END, f"Future Value (Multiple Compounding) = {FV_multi:.4f}\n\n")
                calculations_performed += 1
            except ZeroDivisionError:
                self.result_text.insert(tk.END, "Error: Compounding periods (m) cannot be zero\n\n")
        # Present Value months
        if provided['FV'] and provided['r'] and provided['n'] and provided['m']:
            # PV = FV / (1+(r/m))^(m*n)
            try:
                PV_multi = FV / ((1 + (r / m)) ** (m * n))
                self.result_text.insert(tk.END, f"Present Value (Multiple Compounding) = {PV_multi:.4f}\n\n")
                calculations_performed += 1
            except ZeroDivisionError:
                self.result_text.insert(tk.END, "Error: Division by zero in Present Value calculation\n\n")
        
        # Continuous compounding/discounting
        if provided['PV'] and provided['r'] and provided['n']:
            # FV = PV*e^(r*n)
            FV_continuous = PV * math.exp(r * n)
            self.result_text.insert(tk.END, f"Future Value (Continuous Compounding) = {FV_continuous:.4f}\n\n")
            calculations_performed += 1
        
        # Effective Interest Rate
        if provided['r'] and provided['m'] and provided['n']:
            # re = (1+(r/m))^(m*n)
            try:
                re = ((1 + (r / m)) ** (m * n)) - 1
                self.result_text.insert(tk.END, f"Effective Interest Rate = {re:.4f}\n\n")
                calculations_performed += 1
            except ZeroDivisionError:
                self.result_text.insert(tk.END, "Error: Compounding periods (m) cannot be zero\n\n")
        
        # Unknown Interest Rate
        if provided['FV'] and provided['PV'] and provided['n']:
            # r = ((FV/PV)^(1/n))-1
            try:
                r_unknown = ((FV / PV) ** (1 / n)) - 1
                self.result_text.insert(tk.END, f"Interest Rate = {r_unknown:.4f}\n\n")
                calculations_performed += 1
            except (ValueError, ZeroDivisionError):
                self.result_text.insert(tk.END, "Error in Interest Rate calculation\n\n")
        
        # Unknown Time Period
        if provided['FV'] and provided['PV'] and provided['r']:
            # n = ln(FV/PV)/ln(1+r)
            try:
                n_unknown = math.log(FV / PV) / math.log(1 + r)
                self.result_text.insert(tk.END, f"Time Period = {n_unknown:.4f} years\n\n")
                calculations_performed += 1
            except (ValueError, ZeroDivisionError):
                self.result_text.insert(tk.END, "Error in Time Period calculation\n\n")
        
        # Annuity (Same PMT over same periods)
        if provided['PMT'] and provided['r'] and provided['n']:
            try:
                # FVA = PMT((((1+r)^n)-1)/r)
                FVA = PMT * ((((1 + r) ** n) - 1) / r)
                self.result_text.insert(tk.END, f"Future Value of Annuity = {FVA:.4f}\n")
                
                # PVA = PMT((1-(1+r)^(-n))/r)
                PVA = PMT * ((1 - (1 + r) ** (-n)) / r)
                self.result_text.insert(tk.END, f"Present Value of Annuity = {PVA:.4f}\n\n")
                calculations_performed += 1
                
                # Annuity due - regular payments
                # FV = PMT*((((1+r)^n)-1)/r)*(1+r)
                FV_annuity_due = PMT * ((((1 + r) ** n) - 1) / r) * (1 + r)
                self.result_text.insert(tk.END, f"Future Value of Annuity Due = {FV_annuity_due:.4f}\n")
                
                # PV = PMT((1-(1+r)^(-n))/r)*(1+r)
                PV_annuity_due = PMT * ((1 - (1 + r) ** (-n)) / r) * (1 + r)
                self.result_text.insert(tk.END, f"Present Value of Annuity Due = {PV_annuity_due:.4f}\n\n")
                calculations_performed += 1
            except ZeroDivisionError:
                self.result_text.insert(tk.END, "Error: Interest rate (r) cannot be zero for annuity calculations\n\n")
        
        # Bond Price
        if provided['PMT'] and provided['r'] and provided['n'] and provided['F']:
            try:
                # P = PMT*( (1-(1+r)^(-n))/r )+(F/((1+r)^n))
                bond_price = PMT * ((1 - (1 + r) ** (-n)) / r) + (F / ((1 + r) ** n))
                self.result_text.insert(tk.END, f"Bond Price = {bond_price:.4f}\n\n")
                calculations_performed += 1
            except ZeroDivisionError:
                self.result_text.insert(tk.END, "Error in Bond Price calculation\n\n")
        
        # Constant perpetuity
        if provided['C'] and provided['r']:
            try:
                # PV = C / r
                PV_perpetuity = C / r
                self.result_text.insert(tk.END, f"Present Value of Constant Perpetuity = {PV_perpetuity:.4f}\n\n")
                calculations_performed += 1
            except ZeroDivisionError:
                self.result_text.insert(tk.END, "Error: Interest rate (r) cannot be zero for perpetuity calculations\n\n")
        
        # Growing Perpetuity
        if provided['C'] and provided['r'] and provided['g']:
            try:
                if r > g:
                    # PV = C / (r-g)
                    PV_growing = C / (r - g)
                    self.result_text.insert(tk.END, f"Present Value of Growing Perpetuity = {PV_growing:.4f}\n\n")
                    calculations_performed += 1
                else:
                    self.result_text.insert(tk.END, "Error: Interest rate (r) must be greater than growth rate (g)\n\n")
            except ZeroDivisionError:
                self.result_text.insert(tk.END, "Error: (r-g) cannot be zero for growing perpetuity\n\n")
        
        # Capitalization rate
        if provided['net_income'] and provided['V']:
            try:
                # r = Net Income / V
                cap_rate = net_income / V
                self.result_text.insert(tk.END, f"Capitalization Rate = {cap_rate:.4f}\n\n")
                calculations_performed += 1
            except ZeroDivisionError:
                self.result_text.insert(tk.END, "Error: Value (V) cannot be zero for capitalization rate\n\n")
        
        # Capitalization rate Valuation
        if provided['net_income'] and provided['r']:
            try:
                # V = Net Income / r
                cap_value = net_income / r
                self.result_text.insert(tk.END, f"Capitalization Value = {cap_value:.4f}\n\n")
                calculations_performed += 1
            except ZeroDivisionError:
                self.result_text.insert(tk.END, "Error: Interest rate (r) cannot be zero for capitalization value\n\n")
        
        if calculations_performed == 0:
            self.result_text.insert(tk.END, "No calculations could be performed with the provided values.\n")
            self.result_text.insert(tk.END, "Please enter appropriate values and try again.\n")
        else:
            self.result_text.insert(tk.END, f"Total calculations performed: {calculations_performed}\n")
        
        self.status.config(text=f"Completed {calculations_performed} calculations")
    
    def clear_all(self):
        """Clear all input fields and results"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
            entry.insert(0, "0")
        
        self.result_text.delete(1.0, tk.END)
        self.status.config(text="All fields cleared")
    
    def show_help(self):
        """Show available calculations and required variables"""
        help_window = tk.Toplevel(self.root)
        help_window.title("Available Calculations")
        help_window.geometry("700x500")
        
        help_text = scrolledtext.ScrolledText(help_window, wrap=tk.WORD)
        help_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        help_content = """
AVAILABLE FINANCIAL CALCULATIONS
===============================

1. Capital Asset Pricing Model (CAPM)
   Required: rf_rate, beta, market_premium
   Formula: Expected Return = Risk-Free Rate + β × Market Risk Premium

2. Standard Deviation of Returns
   Required: Returns data (comma or space separated)
   Formula: σ = √[Σ(ri - r̄)² / (n-1)]
   Where:
   - ri is each individual return
   - r̄ is the mean return
   - n is the number of returns

3. Annual Holding Period Yield (HPY)
   Required: BV, EV, n (and optionally c)
   Formula: HPY = ((EV+c)/BV)^(1/n) - 1

4. Credit Multiplier
   Required: reserve_ratio
   Formula: 1 / reserve_ratio

5. Simple Interest
   Required: PV, r, n
   Formula: I = PV * r * n

6. Future Value of single payment (Simple Interest)
   Required: PV, r, n
   Formula: FV = PV(1 + r*n)

7. Present Value of single payment (Simple Interest)
   Required: FV, r, n
   Formula: PV = FV / (1 + r*n)

8. Future Value (Compound Interest)
   Required: PV, r, n
   Formula: FV = PV(1+r)^n

9. Present Value (Compound Interest)
   Required: FV, r, n
   Formula: PV = FV / (1+r)^n

10. Future Value (Multiple Compounding)
    Required: PV, r, n, m
    Formula: FV = PV*(1+(r/m))^(m*n)

11. Present Value (Multiple Compounding)
    Required: FV, r, n, m
    Formula: PV = FV / (1+(r/m))^(m*n)

12. Future Value (Continuous Compounding)
    Required: PV, r, n
    Formula: FV = PV*e^(r*n)

13. Effective Interest Rate
    Required: r, m, n
    Formula: re = (1+(r/m))^(m*n) - 1

14. Unknown Interest Rate
    Required: FV, PV, n
    Formula: r = ((FV/PV)^(1/n))-1

15. Unknown Time Period
    Required: FV, PV, r
    Formula: n = ln(FV/PV)/ln(1+r)

16. Future and Present Value of Annuity
    Required: PMT, r, n
    Formulas: 
    - FVA = PMT((((1+r)^n)-1)/r)
    - PVA = PMT((1-(1+r)^(-n))/r)

17. Future and Present Value of Annuity Due
    Required: PMT, r, n
    Formulas:
    - FV = PMT*((((1+r)^n)-1)/r)*(1+r)
    - PV = PMT((1-(1+r)^(-n))/r)*(1+r)

18. Bond Price
    Required: PMT, r, n, F
    Formula: P = PMT*((1-(1+r)^(-n))/r)+(F/((1+r)^n))

19. Present Value of Constant Perpetuity
    Required: C, r
    Formula: PV = C / r

20. Present Value of Growing Perpetuity
    Required: C, r, g (where r > g)
    Formula: PV = C / (r-g)

21. Capitalization Rate
    Required: Net Income, V
    Formula: r = Net Income / V

22. Capitalization Value
    Required: Net Income, r
    Formula: V = Net Income / r

VARIABLE DEFINITIONS
===================
PV = Present Value
FV = Future Value
r = Interest rate (as decimal, e.g., 0.05 for 5%)
n = Number of years
m = Compounding periods per year
PMT = Regular payment amount
C = Constant payment for perpetuity
g = Growth rate (as decimal)
F = Face value for bond
Net Income = Net income for capitalization calculations
V = Value for capitalization calculations
BV = Beginning Value for HPY calculation
EV = Ending Value for HPY calculation
c = Cash flows (intermediate payments) for HPY calculation
Returns = A series of returns (as decimals) for standard deviation calculation
rf_rate = Risk-Free Rate (as decimal)
beta = Beta coefficient for an asset
market_premium = Market Risk Premium (as decimal)
"""
        
        help_text.insert(tk.END, help_content)
        help_text.config(state=tk.DISABLED)

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = FinancialCalculatorApp(root)
    root.geometry("1500x1000")
    root.resizable(False, False)  # Prevent resizing
    sv_ttk.set_theme("dark")
    root.mainloop()