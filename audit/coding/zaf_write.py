import os, csv
ROOT = r"D:\papers\done\Libya_DT_six_country_study\audit"
EV = os.path.join(ROOT, "evidence", "ZAF")
os.makedirs(EV, exist_ok=True)
A = "2026-11-22"

E = {}
E["S01"] = ("""https://www.dha.gov.za/index.php/civic-services/birth-certificates
https://www.gov.za/services/services-residents/birth/register-birth
https://www.dha.gov.za/index.php/ask-us
https://www.dha.gov.za/index.php/civic-services/dha-stationed-at-hospitals""",
"""[DHA, Birth Certificates & Registration] "Births must be registered within 30 days ... The parent(s), next of kin, or legal guardian of the child must visit the nearest Home Affairs office or the nearest South African embassy or consulate if the client is abroad. Proof of birth from the health facility where the birth occurred (Form DHA 24/PB - a Home Affairs form provided at a health facility). ... Once the child's birth has been registered, a birth certificate with full details of the child and parent(s) is issued free of charge." Late registration: "ID/Passport of parent(s)."
[gov.za, Register birth] "The birth can be registered by a parent, guardian or any other person legally responsible for the child at an office of the Department of Home Affairs. ... Find out more about how to register a birth, or contact the Department of Home Affairs." (links to dha.gov.za)
[DHA Ask us] "What is the waiting period for unabridged birth certificate? It can take between three to eight weeks"
[DHA] Page "DHA Available at Hospitals" lists hospitals/clinics with DHA offices.
No online application for birth registration found on dha.gov.za, eHomeAffairs (ID and passport only) or myhomeaffairsonline.dha.gov.za.""")
E["S02"] = ("""https://ehome.dha.gov.za/ehomeaffairsv3
https://www.dha.gov.za/index.php/id-smart-card/banks-digital
https://www.dha.gov.za/index.php/civic-services/identity-documents
https://www.dha.gov.za/index.php/statements-speeches/2112-bank-branches-750
https://www.gov.za/services/services-residents/citizenship/personal-identification/apply-for-identity-document""",
"""[eHomeAffairs] "eHomeAffairs allows the following: Submit ID and Passport applications online, Make online payments for applications, Make bookings where allowed. Note: (A branch visit is mandatory to capture and/or verify your biometric details, i.e. photo, fingerprints and signature)." Logon: "username (ID Number) and password ... A one-time-pin (OTP) will be sent to your cellphone".
[DHA Banks - Digital] "customers do not need to log onto eHomeAffairs to make bookings or payments. Instead, the service is provided directly through participating banks. ... What do I need to bring when applying? You do not need to bring any documents. How much does it cost? The Department of Home Affairs charges R140 for a Smart ID card. ... Collections will be done at the bank branch where the application was made." "First-time ID applications must be done at a Home Affairs office."
[DHA Identity documents] First-time applicant: "A certified copy of a birth certificate ... No payment is required"; "The fee for the re-issue is R140.00". "The Department uses the cellphone number ... to send you updates about progress".
[DHA statement 11 Nov 2026] "Citizens can simply walk into a participating branch of ABSA, Capitec, First National Bank or Standard Bank".""")
E["S03"] = ("""https://ehome.dha.gov.za/ehomeaffairsv3
https://www.dha.gov.za/index.php/statements-speeches/2116-triples-passport
https://www.dha.gov.za/index.php/civic-services/travel-documents
https://www.gov.za/services/services-residents/travel-outside-sa/apply-passport-or-travel-document
https://myhomeaffairsonline.dha.gov.za/""",
"""[DHA statement, 18 Nov 2026] "passport applications for adults older than 18 officially going live at 480 bank branches ... expanding from just 228 Home Affairs offices to an unprecedented 708 service locations ... the new passport application process involves no prior bookings, paperwork, or queues. ... the next phase ... as well as secure courier delivery of Smart ID Cards and passports for the first time."
[eHomeAffairs] "Submit ID and Passport applications online, Make online payments for applications, Make bookings where allowed. Note: (A branch visit is mandatory to capture and/or verify your biometric details ...)".
[DHA Travel documents] "Ordinary Tourist Passports ... The turnaround time for issuance is 13 working days. The applicable tariff is R600 ... Applications ... can be submitted at any Home Affairs front office ..., participating banks ... or through the eHomeAffairs channel. ... A passport application ... must be made in person." Documents: "Your original identity document and a copy".
[myhomeaffairsonline] "Apply for a Smart ID Card re-issue or a Passport directly through a participating Partner Branch".""")
E["S04"] = ("""https://www.dha.gov.za/index.php/civic-services/birth-certificates
https://www.dha.gov.za/index.php/civic-services/marriages
https://www.dha.gov.za/index.php/ask-us
https://www.gov.za/services/services-residents/relationships/getting-married""",
"""Coded on re-issue of unabridged birth / marriage certificates (DHA).
[DHA Birth certificates] "can apply for a re-issue of a birth certificate at a fee of R75 (unabridged birth certificate) and a fee of R20 (abridged birth certificate). The applicant's ID document is required." "The forms mentioned below are provided at Home Affairs offices".
[DHA Marriages] "the Department commenced with the issuance of unabridged marriage certificates on the spot in all offices as of 31 March 2025."
[DHA Ask us] "What is the waiting period for unabridged birth certificate? It can take between three to eight weeks"
[gov.za Getting married] "You can apply for a copy of the marriage certificate from the Department of Home Affairs ... The first issue of an abridged marriage certificate is free, but you will have to pay for a second issue or an unabridged certificate." (links to dha.gov.za)
No online application channel for certificates found.""")
E["S05"] = ("""https://www.cipc.co.za/?page_id=149
https://www.cipc.co.za//wp-content/uploads/2021/03/NEW-E-SERVICES-COMPANY-REGISTRATION-STEP-BY-STEP-GUIDE-V3.3.pdf
https://www.gov.za/services/online-services
https://bizportal.gov.za (certificate error SEC_E_CERT_EXPIRED, not bypassed)""",
"""[CIPC Enterprise registration] "A company registration may vary between R125 and R475 (R125 for a private company ...)". Platforms: "New E-services ... BizPortal ... CIPC Mobile App; Self Service Terminal; Banks (as part of company registration process)". Turnaround: "E-services: 1 working day; Mobile App, Self Service Centre, Bank, BizPortal immediately (service is dependent on payment being made immediately)". E-services list: "COMPANY REGISTRATION ... TRANSACTION STATUS ... CERTIFICATES".
[CIPC guide V3.3] "the only payment option is via credit or debit card." "No supporting documents need to be send via email to CIPC unless one of the directors and/or incorporators are foreign nationals." "Registration certificate of the new company as well as the Memorandum of Incorporation ... is available for download." "Verification is done via the Department of Home Affairs." "Complete your Username (e-mail address and Password." "Call Centre: 086 100 2472".
[gov.za Online services] "Register as a CIPC customer in order to: register a company ... track transaction status" (link to eservices.cipc.co.za).
Conflict: same CIPC page also says "To register for a new company at the cost of R175.00".""")
E["S06"] = ("""https://tbc.tshwane.gov.za/
https://tbc.tshwane.gov.za/information
https://www.e-tshwane.co.za/""",
"""City of Tshwane (capital) coded; JavaScript pages read in Chrome.
[e-Tshwane] "Business Compliance for License and Permit - The City of Tshwane offers online registration for Business Licenses and Permits. Apply Here".
[Tshwane Trading Portal] "Apply for licences, permits and approvals quickly and easily through one trusted portal. ... We are launching the platform on the 11th of September 2026. ... Formal Business - Apply for formal business licensing linked to one of your registered businesses. Avg. processing: 3-5 days ... Track Application - Check the status of your application. ... Contact Us 012 358 4490 ... Business Compliance and Regulation Section (BCR) Office 3rd Floor, Middestad Building".
[Information centre] "All available information downloads 0 files" (no fee or document checklist published).
gov.za: no page or link to Tshwane business licensing found.""")
E["S07"] = ("""https://www.sars.gov.za/types-of-tax/personal-income-tax/filing-season/
https://www.gov.za/services/online-services""",
"""[SARS Filing Season 2026] "Complete and submit your Personal Income Tax Return (ITR12). Use SARS eFiling or the SARS MobiApp." "Less capturing, more prefilled data: Some of your information (like investment income) will already be filled in on your form". "An Auto Assessment is when SARS works out your tax return for you using information already received from: Your employer, Banks, Medical schemes ..." "Gather your supporting documents in advance." "Can I see my refund amount and payment date or the payment due date of the amount owed by me to SARS on eFiling? Yes". "How to make payments to SARS via the SARS MobiApp". "If you have no other choice but to visit a SARS Service Centre, ensure that you have booked your appointment ... You may also visit our Mobile Tax Units".
[gov.za Online services] "SARS eFiling is a free online process for the submission of tax returns and declarations" (link to sarsefiling.co.za).""")
E["S08"] = ("""https://www.e-tshwane.co.za/what-are-the-services
https://www.e-tshwane.co.za/payment-services
https://www.e-tshwane.co.za/help-faqs
https://www.gov.za/services/place-live/municipal-services""",
"""City of Tshwane municipal account (rates, water and electricity).
[e-Tshwane] "e-Tshwane is a secure free online service ... via the internet and mobile devices. ... users can upload meter readings, pay traffic fines, lodge queries, apply for services, view statements, and make payme[nts]".
[Payment services] "e-Tshwane payments are recorded immediately on payment and we issue you with an electronic proof of payment."
[FAQs] "Registration on e-Tshwane and usage of the site is free." Registration needs "Your City of Tshwane municipal account number; Your SA ID number or valid Passport number". "click on the 'Pay selected Accounts' option". "The status for your payment will remain as 'Pending' ... until you have completed the payment release." "call Center on 086 144 4779". "The site currently does not cater for pre-paid electricity".
[gov.za Municipal services] "Contact your local municipality to apply for these services." (no link to e-Tshwane).""")
E["S09"] = ("""https://www.gov.za/services/register-motor-vehicle/renew-motor-vehicle-licence
https://online.natis.gov.za (connection timed out in curl; Chrome error page, 2026-11-22)""",
"""[gov.za Renew motor vehicle licence] "You must renew your motor vehicle licence at your relevant registering authority or at a selected post office near you." "Motorists can renew and pay for vehicle license discs through the ... (NaTIS) online platform. ... Motorists are required to register a profile ... The new disc will be couriered to your address." "Log into the NaTIS platform; Select 'View Motor Renewals'; Choose the licence disc/car; Capture card details of the respective bank and pay". In person: "your identity document; proof of residential address e.g. utility account". "The application is processed on the same day. ... Contact your local licencing office for the cost."
online.natis.gov.za not observed (TCP timeout to port 443).""")
E["S10"] = ("""https://www.up.ac.za/online-application
https://www.up.ac.za/online-application/application-fee
https://www.up.ac.za/online-application/online-application-instructions
https://www.gov.za/services/services-residents/education-and-training/tertiary-education/register-tertiary-institution""",
"""University of Pretoria coded (no central admission; gov.za: "Apply for admission directly to the institution of your choice"). up.ac.za gave HTTP 403 to curl; read in Chrome.
[UP] "Apply online and Upload your ID/Passport and final School results ... Pay your application fee. ... check the UP Student Portal regularly for your application status ... Final admission will be communicated on the UP Student Portal."
[Application fee] "you will need to pay an application fee of R300 for 2027. ... Online credit card payment as part of this application submission".
[Instructions] "The University of Pretoria does not make use of representatives, agents or agencies during the application process."
gov.za links only to DHET, SAQA and TVET sites, not to UP.""")
E["S11"] = ("""https://services.sassa.gov.za/portal/r/sassa/sassa/home
https://services.sassa.gov.za/portal/r/sassa/files/static/v61/ONLINE%20GRANT%20APPLICATION%20POSTER1.jpg
https://www.gov.za/services/child-care-social-benefits/child-support-grant
https://www.sassa.gov.za (connection failed 2026-11-22)""",
"""Coded on Child Support Grant.
[SASSA Services Portal] "Register here to create a personal profile. This will enable you to access the SASSA services." Toll free "0800 60 1011".
[Poster 'Online grant application'] "You can connect to the SASSA services website on any internet capable device." "A One-Time-Pin (OTP) will be sent to your mobile device to confirm registration." "click on 'Apply for a Grant'". "upload the supporting documents". "Some supporting documents must be certified before uploading". "click the SUBMIT DOCUMENTS button! You will now receive a SMS and email confirmation of your submission with an important reference number".
[gov.za Child support grant, published 2014] "Go to the ... (SASSA) office ... your 13 digit-bar-coded identity document (ID) and the child's birth certificate." "It may take up to three months to process your application." "The service is free." (links to services.sassa.gov.za)""")
E["S12"] = ("""https://www.tshwane.gov.za/?p=82100
https://www.tshwane.gov.za/?page_id=21806
https://www.e-tshwane.co.za/land-development""",
"""City of Tshwane coded.
[Media statement 19 Dec 2024] "The City of Tshwane has launched a new electronic system for the submission and processing of building plans. ... (NAPS), went live in December 2024 ... The rollout of NAPS has started in Regions 1 and 4 ... Applicants can access NAPS on the e-Tshwane portal ... email support@e-tshwane.co.za or call 0861 444 779."
[Land Applications] "moving towards automated services that can be tracked and updated online ... Application to approve building plans ... You need a municipal account number to register on e-Tshwane."
No fee schedule, processing time or document checklist found; no gov.za building-permit page.""")
E["portal"] = ("""https://www.gov.za/
https://www.gov.za/services/online-services
https://www.gov.za/terms-and-conditions-use-0
https://www.gov.za/sa-government-online-website-feedback
http://web.archive.org/cdx/search/cdx?url=www.gov.za&limit=3
http://web.archive.org/web/20211206002859/https://www.gov.za/services/online-services""",
"""[gov.za] "Online Services: Some transactions with government can be completed online". Header "Search gov.za". Footer "Feedback", "Terms and conditions", "Android mobile app", "Apple mobile app".
[Terms] "Privacy ... The privacy statement applies to the GCIS and any legal entity, which control, verify or make use of information that may be collected via this site."
[Feedback] "SA Government Online website feedback".
No accessibility statement, open-data link or national single sign-on found.
P2: portal states no total; own count of Online Services entries = 43 (2026-11-22).
P9: Wayback CDX earliest "za,gov)/ 19941105134618 http://www.gov.za:80/".
P10: capture 20211206002859 of /services/online-services lists 35 entries.""")

for k, (urls, ex) in E.items():
    with open(os.path.join(EV, k + ".txt"), "w", encoding="utf-8") as f:
        f.write(f"Evidence ID: ZAF_{k}\nCountry: South Africa (ZAF)\nCoder: AI-A\nAccess date: {A}\nURLs:\n{urls}\n\nExcerpt (verbatim, official sources):\n{ex}\n")

H = ["ISO3","Country","Service code","Service","Responsible agency","Service page URL","Access date","Coder","Access status",
     "C1","C2","C3","C4","C5","C6","C7","C8","C9","C10","C11","C12","Evidence IDs","Notes"]
L = "C6 and C7 both refer to English."
R = [
 ("S01","Birth registration / birth certificate","Department of Home Affairs (DHA)","https://www.dha.gov.za/index.php/civic-services/birth-certificates","OK",
  ["1","NA","NA","0","1","1","1","1","1","1","NA","0"], "In person at DHA office (incl. DHA offices in hospitals); no online channel found. C4=0: parents' ID required. C10: free + 3-8 weeks (DHA FAQ, unabridged certificate). C5=1: gov.za summary page links to DHA. " + L),
 ("S02","National ID card: first issue or renewal","Department of Home Affairs (DHA); partner banks","https://ehome.dha.gov.za/ehomeaffairsv3","OK",
  ["2","1","1","2","1","1","1","1","1","0","","1"], "eHomeAffairs: apply + pay + book online; branch visit for biometrics mandatory; collection in person. C2=1: ID number + password + OTP. C4=2 for re-issue at banks ('You do not need to bring any documents'); first issue at DHA office still needs certified birth certificate copy. C10=0: fee R140 stated, no processing time. C11 blank: login required, not observed (DHA sends SMS updates). C12=1: 750+ bank branches. " + L),
 ("S03","Passport renewal","Department of Home Affairs (DHA); partner banks","https://ehome.dha.gov.za/ehomeaffairsv3","OK",
  ["2","1","1","2","1","1","1","1","1","1","","1"], "Pilot provisional C1 '1 or 2' resolved as 2: eHomeAffairs allows online application, payment and booking; biometrics in person; courier delivery only planned (statement 18 Nov 2026). C4=2 per statement 'no prior bookings, paperwork, or queues'; conflicts with DHA travel-documents page requiring original ID and copy at offices (most recent coded). C10: 13 working days, R600. C11 blank: login required, not observed. C12=1: 480 bank branches. " + L),
 ("S04","Civil-status extract (e.g. family record, marriage certificate)","Department of Home Affairs (DHA)","https://www.dha.gov.za/index.php/civic-services/birth-certificates","OK",
  ["1","NA","NA","0","1","1","1","1","1","1","NA","0"], "Coded on re-issue of unabridged birth/marriage certificate; in person at DHA office, no online channel found. C4=0: ID document required. C10: R75 + 3-8 weeks (DHA FAQ). " + L),
 ("S05","Company (business) registration","Companies and Intellectual Property Commission (CIPC)","https://www.cipc.co.za/?page_id=149","OK",
  ["3","1","1","2","1","1","1","1","1","1","1","1"], "CIPC new e-services: card payment, DHA verification of directors, registration certificate downloadable. bizportal.gov.za returned an expired certificate (not bypassed). C2=1: CIPC customer account. C8=1: CIPC mobile app. C12=1: banks register companies as part of the process; self-service terminals. Fee conflict on CIPC page: R125 vs R175 (R125 coded section). " + L),
 ("S06","Commercial or business activity licence","City of Tshwane Metropolitan Municipality (Business Compliance and Regulation)","https://tbc.tshwane.gov.za/","OK",
  ["2","1","","NA","0","1","1","1","1","0","1","0"], "Capital city (Tshwane/Pretoria) coded. Online application portal launched 11 Sep 2026; decision delivery not stated. C2=1: portal login (type not observed). C3 blank: no fee published. C4=NA: checklist library empty (0 files). C10=0: processing time 3-5 days stated, fee not. C5=0: no gov.za link. " + L),
 ("S07","Income or corporate tax filing and payment","South African Revenue Service (SARS)","https://www.sars.gov.za/types-of-tax/personal-income-tax/filing-season/","OK",
  ["3","1","1","1","1","1","1","1","1","0","1","0"], "eFiling/MobiApp filing, payment and ITA34 assessment online. C4=1: prefilled third-party data and auto-assessment, but supporting documents may still be requested. C10=0: free (gov.za) but no processing time. C11=1: refund amount/payment date and auto-assessment status visible online. C12=0: tax practitioners not counted. " + L),
 ("S08","Electricity bill payment (public utility)","City of Tshwane Metropolitan Municipality (e-Tshwane)","https://www.e-tshwane.co.za/payment-services","OK",
  ["3","1","1","NA","0","1","1","1","1","1","1","0"], "Capital city coded (municipal account incl. electricity). Online payment with immediate electronic proof of payment; prepaid electricity not available on e-Tshwane. Eskom directly-supplied areas not coded. C4=NA: no document requirements. C10: free to use, recorded immediately. C5=0: gov.za municipal page gives no link. " + L),
 ("S09","Vehicle registration renewal","Road Traffic Management Corporation (eNaTIS) / registering authorities","https://www.gov.za/services/register-motor-vehicle/renew-motor-vehicle-licence","Blocked (bot check / geo)",
  ["3","1","1","0","1","1","1","1","1","0","","1"], "Scored from gov.za page (accessible). online.natis.gov.za timed out (curl TCP timeout; Chrome error page) on 2026-11-22; retry on two more days needed. gov.za states online renewal, card payment and courier delivery of disc. C4=0: in person ID + proof of address. C10=0: same day, cost not stated. C11 blank: NaTIS not observed. C12=1: selected post offices renew licences. " + L),
 ("S10","Public university admission / enrolment","University of Pretoria (public university)","https://www.up.ac.za/online-application","OK",
  ["3","1","1","0","0","1","1","1","0","0","1","0"], "University of Pretoria coded (Tshwane); SA has no central admission (CAS = information service). Online application, fee payment and admission decision on UP Student Portal; contract and registration also via portal. up.ac.za returned 403 to curl, read in Chrome. C4=0: upload ID and school results. C5=0: gov.za links to DHET/SAQA/TVET only. C9=0: no assisted channel on pages read. C10=0: fee R300, no processing time. " + L),
 ("S11","Social-assistance or social-security benefit application","South African Social Security Agency (SASSA)","https://services.sassa.gov.za/portal/r/sassa/sassa/home","OK",
  ["2","1","NA","0","1","1","1","1","1","1","","0"], "Coded on Child Support Grant. SASSA portal: online application with document upload and SMS/email reference; decision delivery not stated online. www.sassa.gov.za could not be reached. Conflict: gov.za CSG page (2014) says apply in person and forms not online; portal (more recent) coded. C3=NA: free. C10: up to three months, free (gov.za). C11 blank: login required, not observed. " + L),
 ("S12","Building permit","City of Tshwane Metropolitan Municipality (City Planning and Development)","https://www.tshwane.gov.za/?p=82100","OK",
  ["2","1","","NA","0","1","1","1","1","0","1","0"], "Capital city coded. Building plan applications submitted online via e-Tshwane (NAPS), rollout started in Regions 1 and 4 only (Dec 2024); approval delivery not stated. C3 blank: no fee published. C4=NA: no checklist published. C11=1: applications 'tracked and updated online'. C5=0: no gov.za page or link. " + L),
]
with open(os.path.join(ROOT, "coding", "ZAF.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f); w.writerow(H)
    for code, svc, ag, url, st, c, note in R:
        w.writerow(["ZAF","South Africa",code,svc,ag,url,A,"AI-A",st] + c + ["ZAF_" + code, note])

HP = ["ISO3","Country","Portal URL","Access date","Coder","P1","P2","P3","P4","P5","P6","P7","P8","P9","P10","Evidence IDs","Notes"]
with open(os.path.join(ROOT, "coding", "ZAF_portal.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f); w.writerow(HP)
    w.writerow(["ZAF","South Africa","https://www.gov.za",A,"AI-A","1","","1","1","0","1","0","0","1994","35","ZAF_portal",
                "P2 blank: portal states no total; own count of Online Services entries = 43 (2026-11-22). P4: privacy statement in Terms and conditions. P5: no accessibility statement found. P6: website feedback page. P7: no national SSO/eID on gov.za. P8: no open-data portal link found. P9: earliest Wayback capture 1994-11-05. P10: 35 entries on /services/online-services in Wayback capture of 2021-12-06 (20211206002859)."])
print("done")
