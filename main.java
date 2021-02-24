import java.util.*;
import java.io.*;

public class StudentManagementConsole {
    public static void main (String[] args) {
        initiate();
    }
    
    // public ArrayList to store clumn names
    public static ArrayList <String> csvColumns = new ArrayList(Arrays.asList(
        "ID", "Name", "Last Name", "Phone", "Major",
        "Semester", "Year", "Course", "Total Mark", "Grade"
    ));
    
    // store the data from csv file
    public static ArrayList<String> csvData = new ArrayList<>();
    
    // declare inputData array as public array
    public static ArrayList<String> inputData;

    // public variables/objects for csv file
    public static String filePath = "Records.csv";
    public static Scanner input;
    public static Scanner reader;
    
    // initiate the program
    public static void initiate() {
        
        while (true) {
            
            // create new Instance of Scanner
            input = new Scanner(System.in);
            
            // output the menu
            output("menu");
            
            // output choose an option
            System.out.print("\n => Choose an option: ");
            
            // validate input data type
            if (input.hasNextInt()) {
                
                // store the input as variable
                int option = input.nextInt();
                
                // do the following instructions
                switch (option) {
                    case 1:
                        // add student record
                        addRecord();
                        break;
                    case 2:
                        // search student record
                        searchRecord();
                        break;
                    case 3:
                        // modify student record
                        modifyRecord();
                        break;
                    case 4:
                        // delete student record
                        deleteRecord();
                        break;
                    case 5:
                        // exit the program
                        terminate();
                }
            } else {
                // output insert correct value
                output("correctValue");
                input.nextLine();
            }
        } 
    }
    
    // read csv file and save the data in csvData
    public static void readFile() {
        try {
            
            // create new instance of Scanner to read the file
            reader = new Scanner(new BufferedReader(new FileReader(filePath)));
            
            // clear old csvData values
            csvData.clear();
            
            // read the document till the end
            while (reader.hasNext()) {
                // read value in a string
                String inputValue = reader.nextLine();

                // write inputValues into ArrayList and split by comma
                inputData = new ArrayList<>(Arrays.asList(inputValue.split(",")));
                
                // write inputData into csvData
                for (int i = 0; i < inputData.size(); i++) {
                    csvData.add(inputData.get(i));
                }
            }
            
        } catch (Exception e) {
            System.out.println("failed to read");
        }
    }
    
    // write csv file from csvData ArrayList
    public static void writeFile() {
        // create instance of File object
        File file = new File(filePath);
        
        try {
            
            // create instance of FileWriter
            FileWriter writer = new FileWriter (file);
            
            // write data from csvData to csv file
            for (int i = 0 ; i < csvData.size(); i += csvColumns.size()) {
                
                int writeIndex = i;

                for (String index : csvColumns) {

                    // write data to csv file
                    writer.append(csvData.get(writeIndex) + ",");
                    
                    writeIndex++;
                }
                
                writer.append("\n");
            }
            
            writer.flush();
            writer.close();
            
        } catch (IOException e) {
            // output writing failed
            output("writingFailed");
        }
    }
    
    // add student record
    public static void addRecord() {
        
        // create the File object
        File file = new File (filePath);
        
        // create new Instance of Scanner
        input = new Scanner(System.in);
        
        try {
            
            // if the file doesn't exists
            // write the column names
            if (file.length() == 0) {
                
                // create FileWriter object
                FileWriter writer = new FileWriter (file, true);
                
                // insert column names via a for loop
                for (int i = 0; i < csvColumns.size(); i++) {
                    
                    // write column names
                    writer.append(csvColumns.get(i) + ",");
                    
                    // if last column name is written
                    // stop writing and go to the next line
                    if (i == (csvColumns.size() - 1)) {
                        writer.append("\n");
                    }
                }
                
                writer.flush();
                writer.close();
            }
            
            // create FileWriter object
            // write the input data
            FileWriter writer = new FileWriter (file, true);
            
            // insert data via scanner
            System.out.println(""); // add space
            for (int i = 0; i < csvColumns.size(); i++) {
                
                // ask for input
                System.out.print(" •  Insert " + csvColumns.get(i) + ": ");
                
                // store input data from scanner in inputData
                String inputData = input.nextLine();
                
                // write inputData into CSV
                writer.append(inputData + ",");
                
                // if data for last column is written
                if (i == (csvColumns.size() - 1)) {
                    writer.append("\n");
                }
            }
            
            writer.flush();
            writer.close();
            
        } catch (Exception e) {
            // output writing failed
            output("writingFailed");
        }
        
        // output record added
        output("recordAdded");
    }
    
    // search student record
    public static void searchRecord() {
        
        // create new instance of Scanner
        input = new Scanner(System.in);
        
        // enter an ID to search
        System.out.println(""); // add space
        System.out.print(" => Enter an ID to search: ");
        
        // ask for input to search which item
        String searchID = input.nextLine();
        
        // read the csv file
        // save the result to csvData ArrayList
        readFile();
        
        // search csvData ArrayList for desired data
        boolean foundID = false;
        for (int i = csvColumns.size() ; i < csvData.size(); i += csvColumns.size()) {
            if (csvData.get(i).equals(searchID)) { // if found, output the desired values
                
                int foundIndex = i;
                int columnIndex = 0;
                foundID = true;
                
                for (int j = 0; j < csvColumns.size(); j++) {
                    
                    if (j == 0) {
                        System.out.printf(success);
                    }
                    
                    if (j >= 0 && j < csvColumns.size()) {
                        System.out.printf(first + second, csvColumns.get(columnIndex), csvData.get(foundIndex));
                        
                        if (j == csvColumns.size()-1) {
                            System.out.printf(bottom);
                        } else {
                            System.out.printf(middle);
                        }
                    }
                    
                    foundIndex++;
                    columnIndex++;
                }
                
                // output record found
                output("found");
                
            }
        }
        
        if (!foundID) {
            // if not found, output not found
            output("notFound");
        }
    }
    
    // modify student record
    public static void modifyRecord() {
        // create new instance of Scanner
        input = new Scanner(System.in);
        
        System.out.println(""); // add space
        
        // enter an ID to modify
        System.out.print(" => Enter an ID to modify: ");
        
        // ask for input to modify which ID
        String modifyID = input.nextLine();
        
        // read csv file
        // save it in csvData ArrayList
        readFile();
        
        // search csvData ArrayList for desired data
        boolean foundID = false;
        for (int i = csvColumns.size() ; i < csvData.size(); i += csvColumns.size()) {
            if (csvData.get(i).equals(modifyID)) { // if found, update the desired values
                
                int foundIndex = i;
                int columnIndex = 0;
                foundID = true;
                
                System.out.println(""); // add space
                
                for (String index : csvColumns) {
                    
                    // ask for input the new value
                    System.out.print(" •  Insert new " + csvColumns.get(columnIndex) + ": ");
                
                    // store input data from scanner in inputData
                    String inputData = input.nextLine();
                    
                    // update the value in csvData ArrayList
                    csvData.set(foundIndex, inputData);
                    
                    foundIndex++;
                    columnIndex++;
                }
                
            }
        }
        
        if (!foundID) {
            
            // if not found, output not found
            output("notFound");
            
        } else {
            
            // write the modified csvData ArrayList to csv file
            writeFile();
            
            // output record modified
            output("modified");
        }
        
    };
    
    // delete student record
    public static void deleteRecord() {
        // create new instance of Scanner
        input = new Scanner(System.in);
        
        // enter an ID to delete
        System.out.println(""); // add space
        System.out.print(" => Enter an ID to delete: ");
        
        // ask for input to delete which ID
        String deleteID = input.nextLine();
        
        // read csv file
        // save it in csvData ArrayList
        readFile();
        
        // search csvData ArrayList for desired data
        boolean foundID = false;
        for (int i = csvColumns.size() ; i < csvData.size(); i += csvColumns.size()) {
            if (csvData.get(i).equals(deleteID)) { // if found, remove the desired values
                
                int foundIndex = i;
                foundID = true;
                
                csvColumns.stream().forEach((item) -> {
                    // remove the value in csvData ArrayList
                    csvData.remove(foundIndex);
                });
                
            }
        }
        
        if (!foundID) {
            
            // if not found, output not found
            output("notFound");
            
        } else {
            
            // write the modified csvData ArrayList to csv file
            writeFile();
            
            // output record deleted
            output("deleted");
        }
        
    };

    // menu items array
    public static String[] menuItems = {
        "Student Mangement System",
        "Add Student","Search Student",
        "Modify Student", "Delete Student", "Exit"
    };
    
    // styling and template for menu and prompts
    // to be used with prinf() or print()
    public static String
        alert   = "\n╭┈ xxx ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈╮\n",
        success = "\n╭┈ /// ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈╮\n",
        top     = "\n╭┈ ••• ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈╮\n",
        middle  =   "├┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┤\n",
        bottom  =   "╰┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈ ••• ┈╯\n",
        row     =   "┊    %-27s ┊\n",
        first   =   "┊    %10s : ",
        second  =   "%-15s┊\n"
    ;
    
    // output menu Items, success, failure status...
    public static void output(String name) {
        
        String rowBottom = row + bottom;
        
        switch (name)  {
            case "menu": // if user wants to print menu list
                for (int i = 0; i < menuItems.length; i++) {
                    if (i == 0) { // print the header
                        System.out.printf(top + row + middle, menuItems[i]);
                    }
            
                    if (i > 0) { // print each row
                        System.out.printf(row, i + ". " +  menuItems[i]);
                        if (i == menuItems.length-1) {
                            System.out.printf(bottom);
                        }
                    }
                } break;
            case "correctValue":
                System.out.printf(alert   + rowBottom, " Insert Correct Value!  ");
                break;
            case "addingFailed":
                System.out.printf(alert   + rowBottom, "     Adding Failed!     ");
                break;
            case "writingFailed":
                System.out.printf(alert   + rowBottom, "     Writing Failed!    ");
                break;
            case "notFound":
                System.out.printf(alert   + rowBottom, "   Record Not Found!    ");
                break;
            case "recordAdded":
                System.out.printf(success + rowBottom, "     Record Added!      ");
                break;
            case "found":
                System.out.printf(success + rowBottom, "     Record Found!      ");
                break;
            case "modified":
                System.out.printf(success + rowBottom, "    Record Modified!    ");
                break;
            case "deleted":
                System.out.printf(success + rowBottom, "    Record Deleted!     ");
                break;
            case "terminate":
                System.out.printf(success + rowBottom, " Exiting the Program... ");
                break;
            default: break;
        } 
    }
    
    // exit the program
    public static void terminate() {
        
        // output exiting the program...
        output("terminate");
        System.out.println("");
        
        // exit the program
        System.exit(0);
    }
}