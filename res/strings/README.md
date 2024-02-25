# The String resource

If you want to translate the application to a specific language you must create here a **JSON** named after your choosen language code. The application will automatically use the **JSON** that matches the system language.

## The JSON

To start a new **JSON**, it is recomended that you copy the default "en_US.json" and edit only the values and never the **JSON** keys. The keys are used by the application as an id to find the corresponding text. 

Those keys that starts with "lt-" means that it is a "long text", i.e. a multiline text that is located inside a '.txt' file in 'long-texts' directory. For multiline texts it is needed that you create a file inside long-texts, name it like "pt_BR-balloon.txt" (prefix as the lang code), and then you put the file name as value to the 'lt' key.
