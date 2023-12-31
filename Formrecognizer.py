from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

""" This file takes key, endpoint and ID card as input. It extracts the details in the ID and
 return all the details in dictionary format  """
def identify(key,endpoint, doc):
        document_analysis_client = DocumentAnalysisClient(
                endpoint=endpoint, credential=AzureKeyCredential(key))

        with open(doc, "rb") as file:
            poller = document_analysis_client.begin_analyze_document(
                "prebuilt-idDocument", file)

        id_documents = poller.result()
        for idx, id_document in enumerate(id_documents.documents):
            print("--------Recognizing ID document #{}--------".format(idx + 1))
            first_name = id_document.fields.get("FirstName")
            last_name = id_document.fields.get("LastName")
            document_number = id_document.fields.get("DocumentNumber")
            dob = id_document.fields.get("DateOfBirth")
            doe = id_document.fields.get("DateOfExpiration")
            sex = id_document.fields.get("Sex")
            address = id_document.fields.get("Address")
            country_region = id_document.fields.get("CountryRegion")
            region = id_document.fields.get("Region")
            dic = {}
            
            dic["First Name"]= first_name.value if first_name else None
            dic["Last Name"]= last_name.value if last_name else None
            dic["Document Number"]= document_number.value if document_number else None
            dic["Date of Birth"]= dob.value if dob else None
            dic["Date of Expiration"]= doe.value if doe else None
            dic["Sex"]= sex.value if sex else None
            dic["Address"]= address.value if address else None
            dic["Country/Region"]= country_region.value if country_region else None
            dic["Region"]= region.value if region else None
            return dic

            
