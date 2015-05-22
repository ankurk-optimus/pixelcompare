import java.io.File;

/**
 * Contains some methods to list files and folders from a directory
 *
 * @author Loiane Groner
 * http://loiane.com (Portuguese)
 * http://loianegroner.com (English)
 */
class ScriptTagGen {

    /**
     * List all the files and folders from a directory
     * @param directoryName to be listed
     */
    public void listFilesAndFolders(String directoryName){

        File directory = new File(directoryName);

        //get all the files from a directory
        File[] fList = directory.listFiles();

        for (File file : fList){
            System.out.println(file.getName());
        }
    }

    /**
     * List all the files under a directory
     * @param directoryName to be listed
     */
    public void listFiles(String directoryName){

        File directory = new File(directoryName);

        //get all the files from a directory
        File[] fList = directory.listFiles();

        for (File file : fList){
            if (file.isFile()){
                System.out.println(file.getName());
            }
        }
    }

    /**
     * List all the folder under a directory
     * @param directoryName to be listed
     */
    public void listFolders(String directoryName){

        File directory = new File(directoryName);

        //get all the files from a directory
        File[] fList = directory.listFiles();

        for (File file : fList){
            if (file.isDirectory()){
                System.out.println(file.getName());
            }
        }
    }

    /**
     * List all files from a directory and its subdirectories
     * @param directoryName to be listed
     */
    public void listFilesAndFilesSubDirectories(String directoryName, int length, String prefix, String postfix, String type) throws Exception{

        File directory = new File(directoryName);

        //get all the files from a directory
        File[] fList = directory.listFiles();

        for (File file : fList){
            if (file.isFile()){


                String fname = file.getCanonicalPath();
                fname  = fname.substring(length);
                if(fname.indexOf(type)>0){
                  System.out.println(prefix + fname + postfix);
                }


            } else if (file.isDirectory()){
                listFilesAndFilesSubDirectories(file.getAbsolutePath(), length, prefix, postfix, type);
            }
        }
    }

    public static void main (String[] args) throws Exception{

      ScriptTagGen listFilesUtil = new ScriptTagGen();

        final String directoryLinuxMac = args[0];

        System.out.println("\n\n<!-- Modules -->\n");
        listFilesUtil.listFilesAndFilesSubDirectories(directoryLinuxMac, directoryLinuxMac.length(), "<script src=\"", "\"></script>", ".module.js");
        System.out.println("\n\n<!-- Factories -->\n");
        listFilesUtil.listFilesAndFilesSubDirectories(directoryLinuxMac, directoryLinuxMac.length(), "<script src=\"", "\"></script>", ".factory.js");
        System.out.println("\n\n<!-- Services -->\n");
        listFilesUtil.listFilesAndFilesSubDirectories(directoryLinuxMac, directoryLinuxMac.length(), "<script src=\"", "\"></script>", ".service.js");
        System.out.println("\n\n<!-- Directives -->\n");
        listFilesUtil.listFilesAndFilesSubDirectories(directoryLinuxMac, directoryLinuxMac.length(), "<script src=\"", "\"></script>", ".directive.js");
        System.out.println("\n\n<!-- Controllers -->\n");
        listFilesUtil.listFilesAndFilesSubDirectories(directoryLinuxMac, directoryLinuxMac.length(), "<script src=\"", "\"></script>", ".controller.js");
        System.out.println("\n\n<!-- HTML Templates -->\n");
        listFilesUtil.listFilesAndFilesSubDirectories(directoryLinuxMac, directoryLinuxMac.length(), "", "", ".html");

    }
}
