
import {createBrowserRouter,RouterProvider} from 'react-router-dom';
import HomePage from './frontend/pages/home';
import ChatBotPage from './frontend/pages/chatbotpage';


const router= createBrowserRouter([

  {path:'/', element: <HomePage></HomePage>},
  {path:'/chat', element: <HomePage></HomePage>},
  {path:'/chatbot/*', element: <ChatBotPage></ChatBotPage>}
])

function App() {


  return(
    <div>
  <RouterProvider router={router}/>
  </div>
  )

}
  

export default App;
