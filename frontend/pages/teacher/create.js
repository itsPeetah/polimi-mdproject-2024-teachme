import { HeadingL } from '@/components/headings';
import { CancleBtnStyle, InputStyle, SubmitBtnStyle } from '@/components/style';
import Link from 'next/link';
import React, { useState } from 'react';

export default function LoginPage() {
    return (
        // MAIN
        <div className="h-screen bg-art flex flex-col items-center justify-center"
        >
            {/* Container */}
            <div
                className="
                    flex flex-col justify-center items-center
                    bg-slate-900/40 backdrop-blur-md shadow-md p-10 rounded-lg 
                    w-11/12 lg:w-8/12 h-5/6
                "
            >
                <HeadingL text={'Creating New Content'} />
                {/* FORM */}
                <form className="w-1/2 mb-4 flex flex-col gap-6">
                    {/* Level */}
                    <select className={InputStyle()}>
                        <option value={0}>Select Level</option>
                        <option value={'A1'}>A1</option>
                        <option value={'A2'}>A2</option>
                        <option value={'B1'}>B1</option>
                        <option value={'B2'}>B2</option>
                        <option value={'C1'}>C1</option>
                        <option value={'C2'}>C2</option>
                    </select>
                    {/* Topic */}
                    <input
                        type="text"
                        id="topic"
                        placeholder='Topic'
                        className={InputStyle()}
                    />
                    {/* PASSWORD INPUT */}
                    {/* SUBMIT BUTTON */}
                    <button
                        type="submit"
                        className={`${SubmitBtnStyle()} mt-4`}
                    >
                        Create
                    </button>
                    <Link href='/teacher' className={CancleBtnStyle()} >
                        Cancle
                    </Link>
                </form>
            </div>
        </div >
    );
}
