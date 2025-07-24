import streamlit as st
import pandas as pd
from datetime import datetime
import re
import io

# Set page config
st.set_page_config(
    page_title="Professional Email Generator",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

class ProfessionalEmailGenerator:
    def __init__(self):
        # Same company formats as before
        self.company_formats = {
            # Investment Banks
            "Goldman Sachs": "{f}.{l}@gs.com",
            "JPMorgan": "{f}.{l}@jpmorgan.com",
            "Morgan Stanley": "{f}.{l}@morganstanley.com",
            "Credit Suisse": "{f}.{l}@credit-suisse.com",
            "UBS": "{f}.{l}@ubs.com",
            "Citigroup": "{f}.{l}@citi.com",
            "Deutsche Bank": "{f}.{l}@db.com",
            "Barclays": "{f}.{l}@barclays.com",
            "HSBC": "{f}.{l}@hsbc.com",
            "Jefferies": "{fi}{l}@jefferies.com",
            "Lazard": "{f}.{l}@lazard.com",
            "RBC Capital Markets": "{f}.{l}@rbccm.com",
            "Rothschild & Co": "{f}.{l}@rothschildandco.com",
            "Standard Chartered": "{f}.{l}@sc.com",
            
            # French Banks
            "BNP Paribas": "{f}.{l}@bnpparibas.com",
            "BNP Paribas UK": "{f}.{l}@uk.bnpparibas.com",
            "Crédit Agricole CIB": "{f}.{l}@ca-cib.com",
            "Société Générale CIB": "{f}.{l}@sgcib.com",
            "Natixis": "{f}.{l}@natixis.com",
            "BPCE": "{f}.{l}@bpce.com",
            "Crédit Mutuel": "{f}.{l}@creditmutuel.fr",
            
            # Hedge Funds & Asset Management
            "Blackstone": "{f}.{l}@blackstone.com",
            "KKR": "{f}.{l}@kkr.com",
            "Apollo": "{f}.{l}@apollo.com",
            "Carlyle": "{f}.{l}@carlyle.com",
            "Bridgewater": "{f}.{l}@bridgewater.com",
            "Two Sigma": "{f}.{l}@twosigma.com",
            "Citadel": "{f}.{l}@citadel.com",
            "Marshall Wace": "{f}.{l}@marshallwace.com",
            "Man Group": "{f}.{l}@man.com",
            "Odey Asset Management": "{f}.{l}@odey.com",
            
            # French Asset Management
            "Amundi": "{f}.{l}@amundi.com",
            "AXA Investment Managers": "{f}.{l}@axa-im.com",
            "Lyxor": "{f}.{l}@lyxor.com",
            "Carmignac": "{f}.{l}@carmignac.com",
            "Tikehau Capital": "{f}.{l}@tikehaucapital.com",
            
            # Consulting
            "McKinsey": "{f}_{l}@mckinsey.com",
            "BCG": "{f}.{l}@bcg.com",
            "Bain": "{f}.{l}@bain.com",
            "Oliver Wyman": "{f}.{l}@oliverwyman.com",
            "Roland Berger": "{f}.{l}@rolandberger.com",
            
            # Big 4
            "Deloitte": "{f}{l}@deloitte.fr",
            "PwC": "{f}.{l}@pwc.com",
            "KPMG": "{f}{l}@kpmg.fr",
            "EY": "{f}.{l}@ey.com",
            
            # Private Equity
            "Advent International": "{f}.{l}@adventinternational.com",
            "Apax Partners": "{f}.{l}@apax.com",
            "CVC Capital": "{f}.{l}@cvc.com",
            "Permira": "{f}.{l}@permira.com",
            "PAI Partners": "{f}.{l}@paipartners.com",
            "Eurazeo": "{f}.{l}@eurazeo.com",
        }
        
        self.categories = {
            "Investment Banks": ["Goldman Sachs", "JPMorgan", "Morgan Stanley", "Credit Suisse", "UBS", "Citigroup", "Deutsche Bank", "Barclays", "HSBC", "Jefferies", "Lazard", "RBC Capital Markets", "Rothschild & Co", "Standard Chartered"],
            "French Banks": ["BNP Paribas", "BNP Paribas UK", "Crédit Agricole CIB", "Société Générale CIB", "Natixis", "BPCE", "Crédit Mutuel"],
            "Hedge Funds & Asset Management": ["Blackstone", "KKR", "Apollo", "Carlyle", "Bridgewater", "Two Sigma", "Citadel", "Marshall Wace", "Man Group", "Odey Asset Management"],
            "French Asset Management": ["Amundi", "AXA Investment Managers", "Lyxor", "Carmignac", "Tikehau Capital"],
            "Consulting": ["McKinsey", "BCG", "Bain", "Oliver Wyman", "Roland Berger"],
            "Big 4": ["Deloitte", "PwC", "KPMG", "EY"],
            "Private Equity": ["Advent International", "Apax Partners", "CVC Capital", "Permira", "PAI Partners", "Eurazeo"]
        }
    
    def clean_name(self, name):
        """Clean and format names"""
        name = re.sub(r'\s+', ' ', name.strip().lower())
        name = re.sub(r"[^\w\s\-']", '', name)
        return name
    
    def generate_email(self, first_name, last_name, company):
        """Generate email based on company format"""
        if company not in self.company_formats:
            raise ValueError(f"Company '{company}' not found in database")
        
        first_clean = self.clean_name(first_name)
        last_clean = self.clean_name(last_name)
        
        format_pattern = self.company_formats[company]
        
        email = format_pattern.format(
            f=first_clean,
            l=last_clean,
            fi=first_clean[0] if first_clean else '',
            li=last_clean[0] if last_clean else ''
        )
        
        return email

# Initialize the generator
@st.cache_resource
def get_generator():
    return ProfessionalEmailGenerator()

generator = get_generator()

# Initialize session state for contacts
if 'contacts' not in st.session_state:
    st.session_state.contacts = []

# Header
st.title("📧 Professional Email Generator")
st.markdown("---")

# Sidebar for navigation
st.sidebar.title("🚀 Navigation")
page = st.sidebar.selectbox(
    "Choose a page:",
    ["Add Contact", "View Contacts", "Company Database", "Export/Import"]
)

# PAGE 1: ADD CONTACT
if page == "Add Contact":
    st.header("➕ Add New Contact")
    
    col1, col2 = st.columns(2)
    
    with col1:
        first_name = st.text_input("First Name *", placeholder="Jean")
        last_name = st.text_input("Last Name *", placeholder="Dupont")
        
        # Company selection with categories
        st.subheader("Select Company")
        category = st.selectbox("Category:", list(generator.categories.keys()))
        company = st.selectbox("Company:", generator.categories[category])
        
    with col2:
        position = st.text_input("Position", placeholder="Analyst")
        source = st.text_input("Source", placeholder="LinkedIn")
        language = st.selectbox("Language", ["FR", "EN", "ES", "DE", "IT"], index=0)
        custom_message = st.text_area("Custom Message", placeholder="Interested in M&A opportunities...", height=100)
    
    # Preview email generation
    if first_name and last_name and company:
        try:
            preview_email = generator.generate_email(first_name, last_name, company)
            st.info(f"📧 Email Preview: **{preview_email}**")
        except Exception as e:
            st.error(f"Error generating email: {e}")
    
    # Add contact button
    if st.button("✅ Add Contact", type="primary"):
        if first_name and last_name and company:
            try:
                email = generator.generate_email(first_name, last_name, company)
                
                contact = {
                    'nom': f"{first_name} {last_name}",
                    'email': email,
                    'entreprise': company,
                    'poste': position,
                    'source': source,
                    'langue': language,
                    'custom_message': custom_message,
                    'date_added': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                st.session_state.contacts.append(contact)
                st.success(f"✅ Contact added: {contact['nom']} - {contact['email']}")
                
                # Clear form
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error: {e}")
        else:
            st.error("❌ Please fill in all required fields (First Name, Last Name, Company)")

# PAGE 2: VIEW CONTACTS
elif page == "View Contacts":
    st.header("👥 View Contacts")
    
    if st.session_state.contacts:
        # Search functionality
        col1, col2 = st.columns([3, 1])
        with col1:
            search_query = st.text_input("🔍 Search contacts...", placeholder="Search by name, company, or email")
        with col2:
            st.write("")  # Spacing
            clear_search = st.button("Clear")
        
        # Filter contacts based on search
        contacts_to_show = st.session_state.contacts
        if search_query:
            query = search_query.lower()
            contacts_to_show = [
                contact for contact in st.session_state.contacts
                if (query in contact['nom'].lower() or 
                    query in contact['entreprise'].lower() or 
                    query in contact['email'].lower())
            ]
        
        # Display contacts count
        st.info(f"📊 Showing {len(contacts_to_show)} of {len(st.session_state.contacts)} contacts")
        
        # Display contacts in a table
        if contacts_to_show:
            df = pd.DataFrame(contacts_to_show)
            # Reorder columns to match your CSV structure
            column_order = ['nom', 'email', 'langue', 'entreprise', 'poste', 'source', 'custom_message', 'date_added']
            # Only include columns that exist in the data
            available_columns = [col for col in column_order if col in df.columns]
            df = df[available_columns]
            
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "nom": "Name",
                    "email": "Email",
                    "langue": "Language",
                    "entreprise": "Company",
                    "poste": "Position",
                    "source": "Source",
                    "custom_message": st.column_config.TextColumn(
                        "Custom Message",
                        width="large"
                    ),
                    "date_added": st.column_config.DatetimeColumn(
                        "Date Added",
                        format="DD/MM/YYYY HH:mm"
                    )
                }
            )
            
            # Delete contacts section
            st.subheader("🗑️ Delete Contact")
            contact_names = [f"{contact['nom']} ({contact['entreprise']})" for contact in contacts_to_show]
            if contact_names:
                contact_to_delete = st.selectbox("Select contact to delete:", [""] + contact_names)
                
                if contact_to_delete and st.button("🗑️ Delete Contact", type="secondary"):
                    # Find and remove the contact
                    for i, contact in enumerate(st.session_state.contacts):
                        if f"{contact['nom']} ({contact['entreprise']})" == contact_to_delete:
                            deleted_contact = st.session_state.contacts.pop(i)
                            st.success(f"✅ Deleted: {deleted_contact['nom']}")
                            st.rerun()
                            break
        else:
            st.warning("No contacts match your search criteria.")
    
    else:
        st.info("📭 No contacts added yet. Go to 'Add Contact' to get started!")

# PAGE 3: COMPANY DATABASE
elif page == "Company Database":
    st.header("🏢 Company Database")
    
    # Display companies by category
    for category, companies in generator.categories.items():
        with st.expander(f"📂 {category} ({len(companies)} companies)"):
            cols = st.columns(2)
            for i, company in enumerate(companies):
                col_idx = i % 2
                with cols[col_idx]:
                    # Show email format
                    format_pattern = generator.company_formats[company]
                    st.write(f"**{company}**")
                    st.code(format_pattern, language=None)
    
    # Add new company section
    st.subheader("➕ Add New Company")
    with st.expander("Add Custom Company"):
        col1, col2 = st.columns(2)
        with col1:
            new_company = st.text_input("Company Name")
            new_category = st.selectbox("Category", list(generator.categories.keys()))
        with col2:
            new_format = st.text_input("Email Format", placeholder="{f}.{l}@company.com")
            st.help("Use {f} for first name, {l} for last name, {fi} for first initial, {li} for last initial")
        
        if st.button("Add Company") and new_company and new_format:
            generator.company_formats[new_company] = new_format
            generator.categories[new_category].append(new_company)
            st.success(f"✅ Added {new_company} to {new_category}")

# PAGE 4: EXPORT/IMPORT
elif page == "Export/Import":
    st.header("💾 Export/Import Data")
    
    # Export section
    st.subheader("📤 Export Contacts")
    if st.session_state.contacts:
        col1, col2 = st.columns(2)
        
        with col1:
            # Download as Excel
            if st.button("📊 Download as Excel", type="primary"):
                df = pd.DataFrame(st.session_state.contacts)
                # Column order to match your CSV structure exactly
                column_order = ['nom', 'email', 'langue', 'entreprise', 'poste', 'source', 'custom_message']
                # Only include columns that exist in the data
                available_columns = [col for col in column_order if col in df.columns]
                df = df[available_columns]
                
                # Create Excel file in memory
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name='Contacts', index=False)
                
                excel_data = output.getvalue()
                
                st.download_button(
                    label="📥 Download Excel File",
                    data=excel_data,
                    file_name=f"contacts_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        
        with col2:
            # Download as CSV
            if st.button("📋 Download as CSV"):
                df = pd.DataFrame(st.session_state.contacts)
                # Column order to match your CSV structure exactly
                column_order = ['nom', 'email', 'langue', 'entreprise', 'poste', 'source', 'custom_message']
                # Only include columns that exist in the data
                available_columns = [col for col in column_order if col in df.columns]
                df = df[available_columns]
                
                csv_data = df.to_csv(index=False)
                
                st.download_button(
                    label="📥 Download CSV File",
                    data=csv_data,
                    file_name=f"contacts_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
    else:
        st.info("📭 No contacts to export. Add some contacts first!")
    
    st.markdown("---")
    
    # Import section
    st.subheader("📤 Import Contacts")
    uploaded_file = st.file_uploader(
        "Choose a file to import",
        type=['xlsx', 'csv'],
        help="Upload an Excel or CSV file with contacts"
    )
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            else:
                df = pd.read_csv(uploaded_file)
            
            st.write("📋 Preview of imported data:")
            st.dataframe(df.head())
            
            if st.button("✅ Import Contacts", type="primary"):
                imported_contacts = df.to_dict('records')
                
                # Add to existing contacts
                for contact in imported_contacts:
                    # Ensure all required fields exist
                    required_fields = ['nom', 'email', 'langue', 'entreprise', 'poste', 'source', 'custom_message']
                    for field in required_fields:
                        if field not in contact:
                            contact[field] = ""
                    
                    if 'date_added' not in contact:
                        contact['date_added'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                st.session_state.contacts.extend(imported_contacts)
                st.success(f"✅ Successfully imported {len(imported_contacts)} contacts!")
                st.rerun()
                
        except Exception as e:
            st.error(f"❌ Error importing file: {e}")
    
    # Clear all data
    st.markdown("---")
    st.subheader("🗑️ Clear All Data")
    st.warning("⚠️ This action cannot be undone!")
    
    if st.button("🗑️ Clear All Contacts", type="secondary"):
        if st.session_state.contacts:
            count = len(st.session_state.contacts)
            st.session_state.contacts = []
            st.success(f"✅ Cleared {count} contacts")
            st.rerun()
        else:
            st.info("No contacts to clear")

# Footer
st.markdown("---")
st.markdown("*Professional Email Generator - Built for networking success! 🚀*")
