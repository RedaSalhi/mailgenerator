import pandas as pd
import re
from datetime import datetime
import os

class ProfessionalEmailGenerator:
    def __init__(self):
        # Dictionary mapping company names to their email formats
        # Format patterns: {f} = first name, {l} = last name, {fi} = first initial, {li} = last initial
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
        
        # Data storage
        self.contacts = []
        
    def clean_name(self, name):
        """Clean and format names"""
        # Remove extra spaces and convert to lowercase
        name = re.sub(r'\s+', ' ', name.strip().lower())
        # Remove special characters but keep hyphens and apostrophes
        name = re.sub(r"[^\w\s\-']", '', name)
        return name
    
    def generate_email(self, first_name, last_name, company):
        """Generate email based on company format"""
        if company not in self.company_formats:
            raise ValueError(f"Company '{company}' not found in database")
        
        # Clean names
        first_clean = self.clean_name(first_name)
        last_clean = self.clean_name(last_name)
        
        # Get format pattern
        format_pattern = self.company_formats[company]
        
        # Replace placeholders
        email = format_pattern.format(
            f=first_clean,
            l=last_clean,
            fi=first_clean[0] if first_clean else '',
            li=last_clean[0] if last_clean else ''
        )
        
        return email
    
    def add_contact(self, first_name, last_name, company, position="", source="", language="fr", custom_message=""):
        """Add a contact to the database"""
        try:
            email = self.generate_email(first_name, last_name, company)
            
            contact = {
                'name': f"{first_name} {last_name}",
                'email': email,
                'company': company,
                'position': position,
                'source': source,
                'language': language,
                'custom_message': custom_message,
                'date_added': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            self.contacts.append(contact)
            print(f"✅ Contact added: {contact['name']} - {contact['email']}")
            return contact
            
        except ValueError as e:
            print(f"❌ Error: {e}")
            return None
    
    def list_companies(self):
        """Display all available companies"""
        print("\n📋 Available Companies:")
        print("=" * 50)
        
        categories = {
            "Investment Banks": ["Goldman Sachs", "JPMorgan", "Morgan Stanley", "Credit Suisse", "UBS", "Citigroup", "Deutsche Bank", "Barclays", "HSBC", "Jefferies", "Lazard", "RBC Capital Markets", "Rothschild & Co", "Standard Chartered"],
            "French Banks": ["BNP Paribas", "BNP Paribas UK", "Crédit Agricole CIB", "Société Générale CIB", "Natixis", "BPCE", "Crédit Mutuel"],
            "Hedge Funds & Asset Management": ["Blackstone", "KKR", "Apollo", "Carlyle", "Bridgewater", "Two Sigma", "Citadel", "Marshall Wace", "Man Group", "Odey Asset Management"],
            "French Asset Management": ["Amundi", "AXA Investment Managers", "Lyxor", "Carmignac", "Tikehau Capital"],
            "Consulting": ["McKinsey", "BCG", "Bain", "Oliver Wyman", "Roland Berger"],
            "Big 4": ["Deloitte", "PwC", "KPMG", "EY"],
            "Private Equity": ["Advent International", "Apax Partners", "CVC Capital", "Permira", "PAI Partners", "Eurazeo"]
        }
        
        for category, companies in categories.items():
            print(f"\n🏢 {category}:")
            for i, company in enumerate(companies, 1):
                print(f"   {i:2d}. {company}")
    
    def search_contacts(self, query=""):
        """Search contacts by name, company, or email"""
        if not query:
            return self.contacts
        
        query = query.lower()
        results = []
        
        for contact in self.contacts:
            if (query in contact['name'].lower() or 
                query in contact['company'].lower() or 
                query in contact['email'].lower()):
                results.append(contact)
        
        return results
    
    def display_contacts(self, contacts=None):
        """Display contacts in a formatted table"""
        if contacts is None:
            contacts = self.contacts
        
        if not contacts:
            print("📭 No contacts found.")
            return
        
        print(f"\n📊 Contacts Database ({len(contacts)} contacts):")
        print("-" * 100)
        print(f"{'Name':<20} {'Email':<35} {'Company':<25} {'Position':<15} {'Message':<20}")
        print("-" * 115)
        
        for contact in contacts:
            name = contact['name'][:19]
            email = contact['email'][:34]
            company = contact['company'][:24]
            position = contact['position'][:14]
            message = contact.get('custom_message', '')[:19]
            print(f"{name:<20} {email:<35} {company:<25} {position:<15} {message:<20}")
    
    def export_to_excel(self, filename=None):
        """Export contacts to Excel file"""
        if not self.contacts:
            print("❌ No contacts to export.")
            return
        
        if filename is None:
            filename = f"contacts_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        try:
            df = pd.DataFrame(self.contacts)
            # Reorder columns as requested
            column_order = ['name', 'email', 'company', 'position', 'source', 'language', 'custom_message', 'date_added']
            df = df[column_order]
            
            df.to_excel(filename, index=False, sheet_name='Contacts')
            print(f"✅ Contacts exported to: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Export failed: {e}")
            return None
    
    def load_from_excel(self, filename):
        """Load contacts from Excel file"""
        try:
            df = pd.read_excel(filename)
            loaded_contacts = df.to_dict('records')
            self.contacts.extend(loaded_contacts)
            print(f"✅ Loaded {len(loaded_contacts)} contacts from {filename}")
            
        except Exception as e:
            print(f"❌ Failed to load from Excel: {e}")

def main():
    """Main interactive function"""
    generator = ProfessionalEmailGenerator()
    
    print("🚀 Professional Email Generator")
    print("===============================")
    
    while True:
        print("\n📋 Options:")
        print("1. Add contact")
        print("2. View all contacts")
        print("3. Search contacts")
        print("4. List available companies")
        print("5. Export to Excel")
        print("6. Load from Excel")
        print("7. Exit")
        
        choice = input("\nSelect option (1-7): ").strip()
        
        if choice == '1':
            print("\n➕ Add New Contact")
            first_name = input("First name: ").strip()
            last_name = input("Last name: ").strip()
            
            generator.list_companies()
            company = input("\nCompany name (exact match): ").strip()
            position = input("Position (optional): ").strip()
            source = input("Source (optional): ").strip()
            language = input("Language (default: fr): ").strip() or "fr"
            custom_message = input("Custom message (optional): ").strip()
            
            generator.add_contact(first_name, last_name, company, position, source, language, custom_message)
            
        elif choice == '2':
            generator.display_contacts()
            
        elif choice == '3':
            query = input("\n🔍 Search query: ").strip()
            results = generator.search_contacts(query)
            generator.display_contacts(results)
            
        elif choice == '4':
            generator.list_companies()
            
        elif choice == '5':
            filename = input("\n💾 Excel filename (optional): ").strip()
            if not filename:
                filename = None
            generator.export_to_excel(filename)
            
        elif choice == '6':
            filename = input("\n📂 Excel filename to load: ").strip()
            if os.path.exists(filename):
                generator.load_from_excel(filename)
            else:
                print("❌ File not found.")
                
        elif choice == '7':
            print("\n👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid option. Please try again.")

# Example usage
if __name__ == "__main__":
    # You can run the interactive version
    # main()
    
    # Or use it programmatically like this:
    generator = ProfessionalEmailGenerator()
    
    # Add some example contacts
    generator.add_contact("Jean", "Dupont", "BNP Paribas", "Analyst", "LinkedIn", "fr", "Interested in M&A opportunities")
    generator.add_contact("Marie", "Martin", "Goldman Sachs", "VP", "Referral", "EN", "Follow-up from networking event")
    generator.add_contact("Pierre", "Dubois", "Société Générale CIB", "Associate", "Company Website", "fr", "Discussing internship possibilities")
    
    # Display contacts
    generator.display_contacts()
    
    # Export to Excel
    generator.export_to_excel("my_contacts.xlsx")
