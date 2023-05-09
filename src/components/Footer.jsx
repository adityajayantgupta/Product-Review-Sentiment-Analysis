import React from 'react'
import {BsFacebook,BsTwitter,BsGithub} from 'react-icons/bs'

const Footer = () => {
  return (
    <footer className='bg-gray-200 p-7 sm:bg-orange-400'>
      <div className=' p-10 flex flex-wrap sm:p-4'>
      <div className='md:flex sm:text-center item-center justify-between w-screen '>
      <div className=''>
      <h3 className='font-medium sm:text-3xl font-serif sm:mb-6'> Freecharge</h3>
      <p className='text-sm py-1 text-gray-400 sm:text-black '>About Us</p>
      <p className='text-sm py-1 text-gray-400 sm:text-black'>Contact Us</p>
      <p className='text-sm py-1 text-gray-400 sm:text-black'>Home</p>
      <p className='text-sm py-1 text-gray-400 sm:text-black'>Customer Care</p>
      <p className='text-sm py-1 text-gray-400 sm:text-black'>Help</p>
      </div>
      <div className='sm:hidden'>
      <h3 className='font-medium'> Freecharge</h3>
      <p className='text-sm py-1 text-gray-400'>About Us</p>
      <p className='text-sm py-1 text-gray-400'>About Us</p>
      <p className='text-sm py-1 text-gray-400'>About Us</p>
      <p className='text-sm py-1 text-gray-400'>About Us</p>
      <p className='text-sm py-1 text-gray-400'>About Us</p>
      </div>
      <div className='sm:hidden'>
      <h3 className='font-medium'> Freecharge</h3>
      <p className='text-sm py-1 text-gray-400'>About Us</p>
      <p className='text-sm py-1 text-gray-400'>About Us</p>
      <p className='text-sm py-1 text-gray-400'>About Us</p>
      <p className='text-sm py-1 text-gray-400'>About Us</p>
      <p className='text-sm py-1 text-gray-400'>About Us</p>
      </div>
      <div className='sm:hidden'>
      <h3 className='font-medium'> Freecharge</h3>
      <p className='text-sm py-1 text-gray-400'>About Us</p>
      <p className='text-sm py-1 text-gray-400'>About Us</p>
      <p className='text-sm py-1 text-gray-400'>About Us</p>
      <p className='text-sm py-1 text-gray-400'>About Us</p>
      <p className='text-sm py-1 text-gray-400'>About Us</p>
      </div>
      </div>
      </div>
      {/*socials*/}
      <div className='flex justify-center gap-4 p-4'>
        <BsFacebook className=' bg-white p-2 text-4xl rounded-md'/>
        <BsTwitter className='bg-white dark:bg-black p-2 text-4xl rounded-md dark:text-white'/>
        <BsGithub className='bg-white dark:bg-black p-2 text-4xl rounded-md dark:text-white'/>
      </div>
      <span className=''>© Harsh Prajapati All Copyright Reserved </span>
    </footer>
  )
}

export default Footer