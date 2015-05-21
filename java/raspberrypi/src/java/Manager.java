import java.io.File;
import java.io.FilenameFilter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.io.Reader;
import java.io.StringWriter;
import static java.lang.Integer.parseInt;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.apache.commons.lang3.StringUtils;
import org.ini4j.Ini;

public class Manager extends HttpServlet
{

   /**
    * 
    */
    private static final long serialVersionUID = -3769486450413693610L;

    public void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException
    {		
        response.setContentType("application/json");	// JSON Output
        response.setHeader( "pragma", "no-cache" );		// Cache aus
        response.setHeader("Cache-Control","no-cache");
        response.setDateHeader("Expires", 0);
        response.setCharacterEncoding("iso-8859-1");
        PrintWriter out = response.getWriter(); 

	String action="";
	if(request.getParameter("action")!="" && request.getParameter("action")!=null){
            action = new String(request.getParameter("action").getBytes("iso-8859-1"), "iso-8859-1");
	}

        if(action.equals("configfilelist"))
        {
            List<String> textFiles = new ArrayList<String>();
            File folder = new File(getServletContext().getRealPath("/")+"python");
                File[] listOfFiles = folder.listFiles();

                for (int i = 0; i < listOfFiles.length; i++) {
                  if (listOfFiles[i].isFile()) {
                    //System.out.println("File " + listOfFiles[i].getName());
                      if (listOfFiles[i].getName().endsWith((".cfg"))) {
                          textFiles.add(listOfFiles[i].getName());
                      }
                  } else if (listOfFiles[i].isDirectory()) {
                    //System.out.println("Directory " + listOfFiles[i].getName());
                  }
                }
         
                /*List<String> textFiles = new ArrayList<String>();
                File dir = new File(getServletContext().getRealPath("/")+"python");
                for (File file : dir.listFiles()) {
                  if (file.getName().endsWith((".cfg"))) {
                    textFiles.add(file.getName());
                  }
                }*/
                System.out.println(textFiles.toString());
                out.println(textFiles);
        }
        
        if(action.equals("configfilelist"))
        {
                List<String> textFiles = new ArrayList<String>();
                File dir = new File(getServletContext().getRealPath("/")+"python");
                for (File file : dir.listFiles()) {
                  if (file.getName().endsWith((".cfg"))) {
                    textFiles.add(file.getName());
                  }
                }
                out.println(textFiles.toString());
        }
        
        out.flush();
    }

    public void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException
    {
        response.setContentType("application/json");	// JSON Output
        response.setHeader( "pragma", "no-cache" );		// Cache aus
        response.setHeader("Cache-Control","no-cache");
        response.setDateHeader("Expires", 0);
        response.setCharacterEncoding("iso-8859-1");
        PrintWriter out = response.getWriter(); 

	String action="";
	if(request.getParameter("action")!="" && request.getParameter("action")!=null){
            action = new String(request.getParameter("action").getBytes("iso-8859-1"), "iso-8859-1");
	}
        

        /*String sortname="";
        if(request.getParameter("sortname")!="" && request.getParameter("sortname")!=null){
            sortname = new String(request.getParameter("sortname").getBytes("iso-8859-1"), "UTF-8");
            if(sortname == null || sortname == ""){sortname="id";}
        }*/
        
        if(action.equals("configsectionlist"))
        {
            // Get params
            String configfile="";
            if(request.getParameter("configfile")!="" && request.getParameter("configfile")!=null){
                configfile = new String(request.getParameter("configfile").getBytes("iso-8859-1"), "iso-8859-1");
            }

            Ini ini = new Ini(new File(getServletContext().getRealPath("/")+"python/"+configfile));
            Set<String> sectionNames = ini.keySet();
            
            ArrayList<String> tmpsections = new ArrayList<String>();
            String sections = "";
            for (String section : sectionNames) {
                tmpsections.add(section);
            }

            sections = String.join(",", tmpsections);
            
            out.println(sections);
        }
        
        if(action.equals("test"))
        {
            // Get params
            int number1 = 1;
            if(request.getParameter("number1")!="" && request.getParameter("number1")!=null){
                String tmp_number1 = new String(request.getParameter("number1").getBytes("iso-8859-1"), "UTF-8");
                if(StringUtils.isNumericSpace(tmp_number1) && tmp_number1!="0"){ number1=Integer.parseInt(tmp_number1); }
            }
            int number2 = 1;
            if(request.getParameter("number2")!="" && request.getParameter("number2")!=null){
                String tmp_number2 = new String(request.getParameter("number2").getBytes("iso-8859-1"), "UTF-8");
                if(StringUtils.isNumericSpace(tmp_number2) && tmp_number2!="0"){ number2=Integer.parseInt(tmp_number2); }
            }

            try{
                out.println(startPythonScript(getServletContext().getRealPath("/")+"python/test.py", number1, number2));
            }
            catch(Exception e){
                StringWriter errors = new StringWriter();
                e.printStackTrace(new PrintWriter(errors));
                out.println(errors.toString());
            }
        }
        
        out.flush();
    }
   
   public int startPythonScript(String pythonPath, int param1, int param2) throws IOException
   {
         //ProcessBuilder pb = new ProcessBuilder("sudo","python",pythonPath,""+param1,""+param2);
         ProcessBuilder pb = new ProcessBuilder("python",pythonPath,""+param1,""+param2);
         pb.redirectErrorStream(true);
         Process p = pb.start();

         String ret = "";

         Reader reader = new InputStreamReader(p.getInputStream());
         int ch;
         while ((ch = reader.read()) != -1) {
             ret = ret + Character.toString((char) ch);
         }
         reader.close();

         return parseInt(ret.trim());
    }
}