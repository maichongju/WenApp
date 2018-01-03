BLOG_TABLE = "Blogs"

class Blog:
    """
    When create the class, given format for the data must be like this
    (Id, Authorld, Author, Title, Create Time, Title Picture, Picture Id)
    """
    def __init__(self,data):
        """
        Precondition:
            data (list) : list of information for the blog
        """
        # Need to convert to list
        self._Id = data[0]
        self._AuthorId = data[1]
        self._Author = data[2]
        self._Title = data[3]
        self._Create_Time = data[4]
        self._Picture_Id = data[5]
        self._content = data[6]

    def getId(self):
        """
        Function will return the blog id 
        Return :
            (String) : Blog Id
        """
        return self._Id

    def setId(self,Id):
        """
        Function will update the Id for the blog object
        Precondition:
            Id (int) : Id for the Blog Object
        """
        self._Id = Id

    def getAutorId(self):
        """
        Function will return the blog author id
        return:
            (int) : Author Id 
        """
        return self._AuthorId

    def setAuthorId(self,AuthorId):
        """
        Function will set/update the Author Id for the blog object
        Precondition:
            AuthorId (int): AuthorId 
        """
        self._AuthorId = int(AuthorId)

    def getAuthor(self):
        """
        Function will return the Author for the blog
        return :
            (string) : Author
        """
        return self._Author

    def setAuthor(self,Author):
        """
        Funtion will set/update the Author
        Preconfition:
            Author (String) : Author for the blog post
        """
        self._Author = Author

    def getTitle(self):
        """
        Function will return the current blog title
        return :
            (String) : title 
        """
        return self._Title

    def setTitle(self,title):
        """
        Function will set/update the title for the post blog
        Precondition:
            title (String) : title for the blog
        """
        self._Title = title

    def getCreateTime(self):
        """
        Function will return the blog create time 
        return :
            (string) : Blog create time
        """
        return str(self._Create_Time)

    def setCreateTime(self,Time):
        """
        Function will set the Create Time for the blog
        Procondition:
           Time (String) : YYYY-MM-DD HH:MM:SS 
        """
        self._Create_Time = Time

    def getPictureId(self):
        """
        Function will return the pictureId, If the blog do 
        not have the title picture then it will return None
        return :
            (int) if the blog has title picture then it will title picture
        """
        if self._Picture_Id.isdigit():
            return _Picture_Id
        else:
            return None

    def setPictureId(self,Id):
        """
        Function set/update Picture Id for the Blog
        Precondition:
            Id (int) :If no picture then set it as NULL, otherwise set the picture Id
        """
        self._Picture_Id = Id

    def getContent(self):
        """
        Function will return the content from the blog object
        return:
            content form the blog
        """
        return self._content

    def setContent(self,content):
        """
        Function will update/set the content for the blog
        Precondition:
            content : content for the blog
        """
        self._content = content



    def getSQLdata(self):
        """
        Function will return the data that can insert into datebase
        """
        return (self._AuthorId,self._Author,self._Title,self._Create_Time,self._Picture_Id,self._content)

class Blogs:
    def __init__(self,database):
        """
        Precondition:
            database (DataBase) : database object for updating database
        """
        self._database = database
        self._size = 20
        self._blogs = self._updateblogs()

    def _updateblogs(self):
        """
        Helper function for getting all the blog 
        """
        GET_STRING = "SELECT * FROM {}".format(BLOG_TABLE)
        datas = self._database.getdata(GET_STRING)
        blogs = []
        for data in datas:
            blogs.append(Blog(data))
        return blogs

    def getblog(self,Id):
        """
        Function will get the blog with the given id
        Precondiftion:
            Id (int)
        return:
            The corrsbon
        """
        GET_STRING = "SELECT * FROM {} WHERE Id={}".format(BLOG_TABLE,Id)
        data = self._database.getdata(GET_STRING)
        if len(data) != 0:
            return Blog(data[0])
        return None

    def getblogs(self):
        """
        Function will return the blogs list 
        return :
            list : list of blog object, Empty will return None
        """
        self._blogs = self._updateblogs()
        if len(self._blogs) == 0:
            return None
        else:
            return self._blogs