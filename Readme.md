# e-Pharmacy-App            <img src="https://d2gg9evh47fn9z.cloudfront.net/800px_COLOURBOX30952395.jpg" height="50" weight="50">

### Project Overview
 - The main idea of this project is to allow users to order medicines online from nearby shops. 
 - The medicine is ordered from the shop which is nearest to the user (or whichever store the user chooses).
 - It not only allows users to get the desired medicine delivered home but also provides the details of the shop from which the medicine is ordered.
 - We used a **Google JavaScript API** which helps us locate the shops using the address provided during registration.
 - We also added a file upload support which converts image to text **(OCR)** through which searching medicines is easier for the user.
 - In addition, we included a **chatbot** for user queries and engaging them in small talk.
 
### Requirements
 - Home Page
   - Top Products
   - New Products
   - Testimonials
   
 - Cart Page
   - Order Summary (Item, Cost, Quantity, Total)
   - Checkout
   - Continue Shopping
   
 - Products Page
   - Filter/ Sort (Alphabetically and based on price)
   - Search items
   - Add items to cart
   - List of all products
   
 - Shop Page
   - List of top shops which are nearest to the user
   - Map displaying the above list of shops
   
 - Payment
   - Paypal payment gateway
 
 - OCR
   - Pytesseract
   - Image to text conversion
 
 - User Profile
   - Authentication ( Login and Register with email verification )
   - Forgot password and reset password
   - Order History of the user
  
 - Shop Profile
   - Allows thw shop owner to add a new medicine into the list (if it does not exist)
   - List of items in the shop
   
 - Chatbot
   - Used DialogFlow ( A natural language understanding program by Google )
   - BotCopy for UI Customization
   - Resolves user queries
   
### What we used

- Backend  : Django Framework (Python based web framework)
- Database : SQLite Database
- Frontend : HTML5, CSS3, Bootstrap
- APIs     : 
  - Nominatim OpenStreet Map API : For conversion of addresses to latitude and longitude
  - Google Maps Javascript API : For displaying the location using marker
  - Django Mail API : For sending user registration verification mails
  - Twilio API : For sending SMS to notify the user after checkout
- OCR : 
  - For converting the prescription image into text 
  - Used Pytesseract wrapper with Tesseract-OCR Engine
- Chatbot : Used DialogFlow and Botcopy
 
 ### Challenges
 
 The twilio API used here could only send SMS to twilio-registered phone numbers. If you want to send SMS to any phonr number you need to subscribe their premium pack.
 
 ### Contributed By:
  - Shreya
  - Prahitha
  - Hemanth
  - Thanuja
  - Sairam
 
  

