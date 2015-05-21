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
import org.ini4j.Profile.Section;

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
                File dir = new File(getServletContext().getRealPath("/")+"python");
                for (File file : dir.listFiles()) {
                  if (file.getName().endsWith((".cfg"))) {
                    textFiles.add(file.getName());
                  }
                }
                out.println(textFiles.toString());
        }
 
        else if(action.equals("pythonfilelist"))
        {
                List<String> textFiles = new ArrayList<String>();
                File dir = new File(getServletContext().getRealPath("/")+"python");
                for (File file : dir.listFiles()) {
                  if (file.getName().endsWith((".py"))) {
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
        
        else if(action.equals("configlist"))
        {
            // Get params
            String configfile="";
            if(request.getParameter("configfile")!="" && request.getParameter("configfile")!=null){
                configfile = new String(request.getParameter("configfile").getBytes("iso-8859-1"), "iso-8859-1");
            }
            
            String configsection="";
            if(request.getParameter("configsection")!="" && request.getParameter("configsection")!=null){
                configsection = new String(request.getParameter("configsection").getBytes("iso-8859-1"), "iso-8859-1");
            }

            Ini ini = new Ini(new File(getServletContext().getRealPath("/")+"python/"+configfile));
            
            ArrayList<String> tmpkeys = new ArrayList<String>();
            String keys = "";
            for (String sectionName: ini.keySet()) {
                Section section = ini.get(sectionName);
                if(sectionName.equals(configsection))
                {
                    for (String optionKey: section.keySet()) {
                        tmpkeys.add(optionKey);
                    }
                }
            }

            keys = String.join(",", tmpkeys);
            
            out.println(keys);
        }
        
        else if(action.equals("configvalue"))
        {
            // Get params
            String configfile="";
            if(request.getParameter("configfile")!="" && request.getParameter("configfile")!=null){
                configfile = new String(request.getParameter("configfile").getBytes("iso-8859-1"), "iso-8859-1");
            }
            
            String configsection="";
            if(request.getParameter("configsection")!="" && request.getParameter("configsection")!=null){
                configsection = new String(request.getParameter("configsection").getBytes("iso-8859-1"), "iso-8859-1");
            }
            
            String configkey="";
            if(request.getParameter("configkey")!="" && request.getParameter("configkey")!=null){
                configkey = new String(request.getParameter("configkey").getBytes("iso-8859-1"), "iso-8859-1");
            }

            Ini ini = new Ini(new File(getServletContext().getRealPath("/")+"python/"+configfile));
            
            String keyvalue = "";
            for (String sectionName: ini.keySet()) {
                Section section = ini.get(sectionName);
                if(sectionName.equals(configsection))
                {
                    for (String optionKey: section.keySet()) {
                        if(optionKey.equals(configkey))
                        {
                            keyvalue=section.get(optionKey);
                        }
                    }
                }
            }

            out.println(keyvalue);
        }
        
        else if(action.equals("setconfigvalue"))
        {
            // Get params
            String configfile="";
            if(request.getParameter("configfile")!="" && request.getParameter("configfile")!=null){
                configfile = new String(request.getParameter("configfile").getBytes("iso-8859-1"), "iso-8859-1");
            }
            
            String configsection="";
            if(request.getParameter("configsection")!="" && request.getParameter("configsection")!=null){
                configsection = new String(request.getParameter("configsection").getBytes("iso-8859-1"), "iso-8859-1");
            }
            
            String configkey="";
            if(request.getParameter("configkey")!="" && request.getParameter("configkey")!=null){
                configkey = new String(request.getParameter("configkey").getBytes("iso-8859-1"), "iso-8859-1");
            }
            
            String newconfigvalue="";
            if(request.getParameter("newconfigvalue")!="" && request.getParameter("newconfigvalue")!=null){
                newconfigvalue = new String(request.getParameter("newconfigvalue").getBytes("iso-8859-1"), "iso-8859-1");
            }

            Ini ini = new Ini(new File(getServletContext().getRealPath("/")+"python/"+configfile));
            
            String keyvalue = "";
            for (String sectionName: ini.keySet()) {
                Section section = ini.get(sectionName);
                if(sectionName.equals(configsection))
                {
                    for (String optionKey: section.keySet()) {
                        if(optionKey.equals(configkey))
                        {
                            ini.put(configsection, configkey, newconfigvalue);
                        }
                    }
                }
            }
            ini.store();
            
            out.println(newconfigvalue);
        }
        
        if(action.equals("run"))
        {
            // Get params
            /*int number1 = 1;
            if(request.getParameter("number1")!="" && request.getParameter("number1")!=null){
                String tmp_number1 = new String(request.getParameter("number1").getBytes("iso-8859-1"), "UTF-8");
                if(StringUtils.isNumericSpace(tmp_number1) && tmp_number1!="0"){ number1=Integer.parseInt(tmp_number1); }
            }
            int number2 = 1;
            if(request.getParameter("number2")!="" && request.getParameter("number2")!=null){
                String tmp_number2 = new String(request.getParameter("number2").getBytes("iso-8859-1"), "UTF-8");
                if(StringUtils.isNumericSpace(tmp_number2) && tmp_number2!="0"){ number2=Integer.parseInt(tmp_number2); }
            }*/

            try{
                //out.println(startPythonScript(getServletContext().getRealPath("/")+"python/test.py", number1, number2));
                out.println(startPythonScript(getServletContext().getRealPath("/")+"python/test.py"));
            }
            catch(Exception e){
                StringWriter errors = new StringWriter();
                e.printStackTrace(new PrintWriter(errors));
                out.println(errors.toString());
            }
        }
        
        out.flush();
    }
   
   public String startPythonScript(String pythonPath) throws IOException
   {
         //ProcessBuilder pb = new ProcessBuilder("sudo","python",pythonPath,""+param1,""+param2);
         ProcessBuilder pb = new ProcessBuilder("python",pythonPath);
         pb.redirectErrorStream(true);
         Process p = pb.start();

         String ret = "";

         Reader reader = new InputStreamReader(p.getInputStream());
         int ch;
         while ((ch = reader.read()) != -1) {
             ret = ret + Character.toString((char) ch);
         }
         reader.close();

         return ret.trim();
    }
}