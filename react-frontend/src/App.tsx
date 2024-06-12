
import {createBrowserRouter,RouterProvider} from 'react-router-dom';
import HomePage from './frontend/pages/home';


const router= createBrowserRouter([

  {path:'/', element: <HomePage></HomePage>},
])

function App() {


  return(
    <div>
  <RouterProvider router={router}/>
  </div>
  )

}
  

export default App;
