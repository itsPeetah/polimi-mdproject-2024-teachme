import Link from 'next/link';
import { useRouter } from 'next/router';
import { React, useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
// APIs
import useSWR from 'swr';
import { getCookie } from 'cookies-next';
// Components
import { HeadingL, HeadingXL } from '@/components/Headings';
import Head from 'next/head';


export default function ManageStudentsPage() {
    // Constants
    const router = useRouter()
    const fetcher = (...args) => fetch(...args).then((res) => res.json())
    // Form Data API
    const { register, handleSubmit } = useForm();
    const { register: register2, handleSubmit: handleSubmit2 } = useForm();
    // States
    const [isError, setIsError] = useState(false)
    const [allStudents, setAllStudents] = useState([])
    const [currentStudents, setCurrentStudents] = useState([])

    // Fetch All Students
    const url1 = 'http://127.0.0.1:5000/get-all-students'
    const { data: allStudentsData, error: error1 } = useSWR(url1, fetcher)
    useEffect(() => {
        if (allStudentsData) {
            setAllStudents(allStudentsData)
        } else if (error1) {
            setIsError(true)
        }
    }, [allStudentsData, error1])

    //  Fetch Current Students
    const url2 = 'http://127.0.0.1:5000/get-friends/' + getCookie('email')
    const { data: allCurrentStudentsData, error: error2 } = useSWR(url2, fetcher)
    useEffect(() => {
        if (allCurrentStudentsData) {
            setCurrentStudents(allCurrentStudentsData)
            console.log(allCurrentStudentsData)
        } else if (error2) {
            setIsError(true)
            console.log(error2)
        }
    }, [allCurrentStudentsData, error2])

    //  Add Student
    const add = async (data) => {
        const url = "http://127.0.0.1:5000/create-friendship"
        try {
            const response = await fetch(url, {
                method: "POST",
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    teacher_email: getCookie('email'),
                    student_email: data.student
                }),
            })
            if (response.ok) {
                alert('Student Added Successfully')
                router.reload()
            } else {
                setIsError(true)
                console.log('error')
            }
        } catch (error) {
            setIsError(true)
            console.log(error)
        }
    };
    //  Remove Student
    const remove = async (data) => {
        const url = "http://127.0.0.1:5000/remove-friendship"
        try {
            const response = await fetch(url, {
                method: "POST",
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    teacher_email: getCookie('email'),
                    student_email: data['remove-student']
                }),
            })
            if (response.ok) {
                alert('Student Removed Successfully')
                router.reload()
            } else {
                setIsError(true)
                console.log('error')
            }
        } catch (error) {
            setIsError(true)
            console.log(error)
        }
    };

    // RENDER
    return (
        // MAIN
        <div
            className="min-h-screen bg-art flex flex-col items-center justify-center"
        >
            <Head>
                <title>TeachMe | Manage Students</title>
            </Head>
            {/* Container */}
            <div
                className="flex flex-col items-center gap-8 bg-slate-900/40 backdrop-blur-md shadow-md p-10 w-full h-full"
            >
                {/* Heading */}
                <HeadingXL text={'Manage Students'} />
                {/* Error */}
                {isError && <h1 className="text-rose-900 font-bold text-2xl">Server Error!</h1>}
                {/* Add Student Section */}
                <section className='w-full md:w-5/6 px-4 py-10 border-4 rounded-2xl'>
                    <HeadingL text={'Add Student'} />
                    {/* FORM */}
                    <form
                        className="sm:w-1/2 mb-4 flex flex-col gap-6 mx-auto"
                        onSubmit={handleSubmit(add)}
                    >
                        <select
                            className='form-input'
                            id='student-to-add'
                            {...register('student', { required: true })}
                        >
                            <option value={''}>
                                Select a Student
                            </option>
                            {allStudents.map((student, index) => (
                                <option key={index} value={student.email}>
                                    {student.username} --- {student.email}
                                </option>
                            ))
                            }
                        </select>
                        {/* SUBMIT BUTTON */}
                        <button
                            type="submit"
                            className='submit-btn'
                        >
                            Add Student
                        </button>
                    </form>
                </section>  {/* Add Student Section */}

                {/* Remove Student Section */}
                <section className='w-full md:w-5/6 px-4 py-10 border-4 rounded-2xl'>
                    <HeadingL text={'Remove Student'} />
                    {/* FORM */}
                    <form
                        className="sm:w-1/2 mb-4 flex flex-col gap-6 mx-auto"
                        onSubmit={handleSubmit2(remove)}
                    >
                        <select
                            className='form-input'
                            id='student-to-remove'
                            {...register2('remove-student', { required: true })}
                        >
                            <option value={''}>Select a Student</option>
                            {currentStudents.map((student, index) => (
                                <option key={index} value={student}>
                                    {student}
                                </option>
                            ))
                            }
                        </select>
                        {/* SUBMIT BUTTON */}
                        <button
                            type="submit"
                            className='cancle-btn'
                        >
                            Remove Student
                        </button>
                    </form>
                </section> {/* Remove Student Section */}
                {/* Close Button */}
                <Link href='/teacher' className='navigation-btn w-80'>
                    Close
                </Link>
            </div> {/* Container */}
        </div > // MAIN
    );
}
